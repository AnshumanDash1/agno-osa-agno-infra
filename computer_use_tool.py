import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from agno.tools import tool

# AppleScript helpers

_OSASCRIPT_PATH: Optional[str] = None


def _get_osascript_path() -> str:
    """Return a usable path to osascript, caching the lookup."""
    global _OSASCRIPT_PATH
    if _OSASCRIPT_PATH:
        return _OSASCRIPT_PATH

    candidate = shutil.which("osascript")
    if candidate:
        _OSASCRIPT_PATH = candidate
        return candidate

    fallback = Path("/usr/bin/osascript")
    if fallback.exists():
        _OSASCRIPT_PATH = str(fallback)
        return _OSASCRIPT_PATH

    raise RuntimeError("Unable to locate the osascript binary on this system")


def run_applescript(script: str, timeout: Optional[int] = None) -> str:
    """Execute AppleScript and return stdout, raising on failure."""
    osascript_path = _get_osascript_path()
    completed = subprocess.run(
        [osascript_path, "-e", script],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        if "Allow JavaScript from Apple Events" in stderr:
            raise RuntimeError(
                "Chrome is blocking AppleScript JavaScript execution. Enable it via "
                "Chrome > View > Developer > Allow JavaScript from Apple Events."
            )
        raise RuntimeError(f"AppleScript failed: {stderr or 'unknown error'}")
    return completed.stdout.strip()


def _escape_for_applescript(js_code: str) -> str:
    """Escape JS so it can be embedded in AppleScript string literals."""
    return (
        js_code.replace("\\", "\\\\")
        .replace("\"", "\\\"")
        .replace("\n", "\\n")
    )


def execute_javascript(js_code: str, timeout: Optional[int] = None) -> str:
    """Run JS in the active Chrome tab and return the string result."""
    safe_js = _escape_for_applescript(js_code)
    script = f'''
    tell application "Google Chrome"
        if not (exists window 1) then
            return ""
        end if
        execute front window's active tab javascript "{safe_js}"
    end tell
    '''
    return run_applescript(script, timeout=timeout)



GMAIL_BASE_URL = "https://mail.google.com/"


def _focus_or_open_gmail(target_url: str = GMAIL_BASE_URL) -> None:
    """Focus an existing Gmail tab or open a new one if none are found."""
    escaped_target = _escape_for_applescript(target_url)
    script = f"""
    tell application "Google Chrome"
        if (count of windows) = 0 then
            make new window
        end if
        set frontWindow to front window

        set activeMatches to false
        try
            set activeUrl to URL of active tab of frontWindow
            if activeUrl contains "mail.google.com" then
                set activeMatches to true
            end if
        on error
            set activeMatches to false
        end try

        if activeMatches then
            activate
            return
        end if

        set foundWindow to missing value
        set foundTabIndex to 0

        set windowCount to count of windows
        repeat with windowIndex from 1 to windowCount
            set currentWindow to window windowIndex
            set tabCount to count of tabs of currentWindow
            repeat with tabIndex from 1 to tabCount
                set currentTab to tab tabIndex of currentWindow
                try
                    set tabUrl to URL of currentTab
                on error
                    set tabUrl to ""
                end try
                if tabUrl contains "mail.google.com" then
                    set foundWindow to currentWindow
                    set foundTabIndex to tabIndex
                    exit repeat
                end if
            end repeat
            if foundWindow is not missing value then exit repeat
        end repeat

        if foundWindow is missing value then
            tell frontWindow
                make new tab with properties {{URL:"{escaped_target}"}}
                set active tab index to (count of tabs)
            end tell
            activate
        else
            set index of foundWindow to 1
            set active tab index of foundWindow to foundTabIndex
            activate
        end if
    end tell
    """
    run_applescript(script)

# Gmail tooling utilities

def _ensure_gmail_loaded(timeout_seconds: int = 10) -> None:
    _focus_or_open_gmail()
    js = """
    (() => {
        const url = window.location.href;
        const atInbox = /mail\.google\.com\/mail/.test(url);
        if (!atInbox) {
            return JSON.stringify({ success: false, message: "Active tab is not Gmail" });
        }
        const inboxRow = document.querySelector('div.Cp tr.zA');
        if (!inboxRow) {
            const backButton = document.querySelector('div[aria-label=\"Back to inbox\"], div[aria-label=\"Back\"]');
            if (backButton) {
                backButton.click();
            } else if (!window.__agnoNavigatedToInbox) {
                window.__agnoNavigatedToInbox = Date.now();
                window.location.href = 'https://mail.google.com/mail/u/0/#inbox';
            }
            return JSON.stringify({ success: false, message: "No message rows detected" });
        }
        return JSON.stringify({ success: true });
    })()
    """
    deadline = time.time() + timeout_seconds
    last_error = "Gmail inbox not ready"
    while time.time() < deadline:
        raw = execute_javascript(js)
        try:
            result = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            last_error = "Unable to verify Gmail state"
        else:
            if result.get("success"):
                return
            last_error = result.get("message", "Gmail inbox not ready")
        time.sleep(0.5)
    raise RuntimeError(last_error)



def _wait_for_condition(js_condition: str, timeout_seconds: int = 10) -> Any:
    """Poll for a condition in Gmail and return its payload when ready."""
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        raw = execute_javascript(js_condition)
        if raw:
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = None
            else:
                if payload and payload.get("ready"):
                    return payload.get("data")
        time.sleep(0.5)
    raise TimeoutError("Timed out waiting for Gmail to load content")


def list_recent_emails(limit: int = 5) -> List[Dict[str, str]]:
    """Return summaries of the most recent Gmail messages in the inbox."""
    _ensure_gmail_loaded()

    js = f"""
    (() => {{
        const rows = Array.from(document.querySelectorAll('div.Cp tr.zA'));
        const seen = new Set();
        const emails = [];
        for (const row of rows) {{
            const threadMeta = row.querySelector('[data-legacy-thread-id]');
            const threadId = threadMeta ? threadMeta.getAttribute('data-legacy-thread-id') : '';
            if (!threadId || seen.has(threadId)) {{
                continue;
            }}
            seen.add(threadId);

            const subjectEl = row.querySelector('span.bog');
            const snippetEl = row.querySelector('span.y2');
            const timeEl = row.querySelector('td.xW span, span.xW span, time');
            const messageId = threadMeta.getAttribute('data-legacy-last-message-id') || '';
            const senders = Array.from(row.querySelectorAll('span.yP'))
                .map(el => el.innerText.trim())
                .filter(Boolean);
            const senderParts = [];
            for (const name of senders) {{
                if (!name || name === ',') {{
                    continue;
                }}
                if (!senderParts.includes(name)) {{
                    senderParts.push(name);
                }}
            }}

            emails.push({{
                subject: subjectEl ? subjectEl.innerText.trim() : '',
                sender: senderParts.join(', '),
                snippet: snippetEl ? snippetEl.innerText.replace(/^\s*-\s*/, '').trim() : '',
                received_at: timeEl ? (timeEl.getAttribute('title') || timeEl.innerText.trim()) : '',
                thread_id: threadId,
                message_id: messageId,
                href: threadId ? 'https://mail.google.com/mail/u/0/#inbox/' + threadId : '',
            }});

            if (emails.length >= {limit}) {{
                break;
            }}
        }}
        return JSON.stringify(emails);
    }})()
    """
    raw = execute_javascript(js)
    try:
        return json.loads(raw) if raw else []
    except json.JSONDecodeError as exc:
        raise RuntimeError("Unable to parse Gmail message list") from exc



def read_email_body(thread_id: str, message_index: int = 0) -> Dict[str, str]:
    """Open a Gmail thread by thread_id and return the specified message body."""
    if not thread_id:
        raise ValueError("thread_id is required")
    _ensure_gmail_loaded()

    js_open = f"""
    (() => {{
        const rows = Array.from(document.querySelectorAll('div.Cp tr.zA'));
        const target = rows.find(row => {{
            const meta = row.querySelector('[data-legacy-thread-id]');
            return meta && meta.getAttribute('data-legacy-thread-id') === '{thread_id}';
        }});
        if (!target) {{
            return JSON.stringify({{ success: false, message: 'Thread not found in current inbox view' }});
        }}
        target.scrollIntoView({{ block: 'center', behavior: 'auto' }});
        const clickable = target.querySelector('div.xS[role="link"], span.bog, td.xY, td.a4W');
        const element = clickable || target;
        element.click();
        return JSON.stringify({{ success: true }});
    }})()
    """
    result = execute_javascript(js_open)
    try:
        parsed = json.loads(result) if result else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError("Unable to navigate to Gmail thread") from exc
    if not parsed.get("success"):
        raise RuntimeError(parsed.get("message", "Failed to open thread"))

    js_wait_body = f"""
    (() => {{
        const messageFrames = Array.from(document.querySelectorAll('div.if iframe')).map(frame => {{
            if (frame.contentDocument) {{
                return frame.contentDocument.querySelector('div.a3s');
            }}
            return null;
        }}).filter(Boolean);
        const inlineMessages = Array.from(document.querySelectorAll('div.a3s.aiL'));
        const messages = messageFrames.length ? messageFrames : inlineMessages;
        if (!messages.length) {{
            return JSON.stringify({{ ready: false }});
        }}
        const index = Math.max(0, Math.min(messages.length - 1, {message_index}));
        const chosen = messages[index];
        if (!chosen) {{
            return JSON.stringify({{ ready: false }});
        }}
        const bodyText = chosen.innerText.trim();
        const subjectEl = document.querySelector('h2.hP');
        const senderEl = document.querySelectorAll('span.gD')[index] || document.querySelector('span.gD');
        const dateEl = document.querySelectorAll('span.g3')[index] || document.querySelector('span.g3');
        return JSON.stringify({{
            ready: true,
            data: {{
                subject: subjectEl ? subjectEl.innerText.trim() : '',
                sender: senderEl ? senderEl.innerText.trim() : '',
                received_at: dateEl ? dateEl.innerText.trim() : '',
                body: bodyText,
                message_index: index,
                thread_id: '{thread_id}'
            }}
        }});
    }})()
    """
    data = _wait_for_condition(js_wait_body)
    return data



def open_chrome_url(url: str) -> None:
    """Open the provided URL in Google Chrome."""
    if not url:
        raise ValueError("url is required")
    if "mail.google.com" in url:
        _focus_or_open_gmail(target_url=url)
        return
    script = f'''
    tell application "Google Chrome"
        if not (exists window 1) then
            make new window
        end if
        tell window 1
            make new tab with properties {{URL:"{url}"}}
            set active tab index to (count of tabs)
        end tell
        activate
    end tell
    '''
    run_applescript(script)


# Tool adapters for Agent runtime

@tool(name="list_recent_emails")
def list_recent_emails_tool(limit: int = 5) -> List[Dict[str, str]]:  # pragma: no cover - thin wrapper
    return list_recent_emails(limit=limit)


@tool(name="read_email_body")
def read_email_body_tool(thread_id: str, message_index: int = 0) -> Dict[str, str]:  # pragma: no cover
    return read_email_body(thread_id=thread_id, message_index=message_index)


@tool(name="open_chrome_url")
def open_chrome_url_tool(url: str) -> None:  # pragma: no cover
    open_chrome_url(url=url)
