import subprocess
import json
from agno.tools import tool


def run_applescript(script):
   subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    ).stdout.strip()

def open_chrome_url(url):
    """
    Open the Chrome browser and a specific url inside the user's local computer.
    Args:
        url: The url to open in the browser.
    :return: nothing
    """

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

def execute_javascript(js_code: str):
    script = f'''
    tell application "Google Chrome"
        if not (exists window 1) then
            return "No Chrome window open"
        end if
        execute front window's active tab javascript "{js_code}"
    end tell
    '''
    return run_applescript(script)



def get_unread_emails(limit: int = 5) -> list[dict]:
    js_code = f"""
    (() => {{
        const rows = document.querySelectorAll('tr.zE'); // unread only
        const emails = [];
        for (let i = 0; i < rows.length && emails.length < {limit}; i++) {{
            const row = rows[i];
            const subjectEl = row.querySelector('span.bog');
            const senderEl = row.querySelector('span.zF, span.yX');
            const snippetEl = row.querySelector('span.y2');
            emails.push({{
                subject: subjectEl ? subjectEl.innerText : "",
                sender: senderEl ? senderEl.innerText : "",
                snippet: snippetEl ? snippetEl.innerText.replace(/^\\s*-\\s*/, "") : ""
            }});
        }}
        return JSON.stringify(emails);
    }})()
    """
    raw = execute_javascript(js_code)
    try:
        return json.loads(raw) if raw else []
    except json.JSONDecodeError:
        return []
