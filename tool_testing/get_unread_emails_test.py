import json
import time
import subprocess

def run_applescript(script: str) -> str:
    p = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    return p.stdout.strip()

def execute_javascript(js_code: str) -> str:
    # Escape for AppleScript
    safe_js = js_code.replace("\\", "\\\\").replace('"', '\\"')
    script = f'''
    tell application "Google Chrome"
        if not (exists window 1) then return ""
        execute front window's active tab javascript "{safe_js}"
    end tell
    '''
    return run_applescript(script)

def get_unread_emails(limit: int = 5) -> list[dict]:
    js_code = f"""
    (() => {{
        const rows = document.querySelectorAll('tr.zE');
        const emails = [];
        for (let i = 0; i < rows.length && emails.length < {limit}; i++) {{
            const row = rows[i];
            const subjectEl = row.querySelector('span.bog');
            const senderEl = row.querySelector('span.zF, span.yX');
            const snippetEl = row.querySelector('span.y2');
            const a = row.querySelector('td a[href]');
            emails.push({{
                subject: subjectEl ? subjectEl.innerText.trim() : "",
                sender: senderEl ? senderEl.innerText.trim() : "",
                snippet: snippetEl ? snippetEl.innerText.replace(/^\\s*-\\s*/, "").trim() : "",
                href: a ? a.href : ""
            }});
        }}
        return JSON.stringify(emails);
    }})()
    """
    raw = execute_javascript(js_code).strip()
    if not raw:
        return []
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # try to clean if AppleScript wrapped in extra quotes
        if raw.startswith('"') and raw.endswith('"'):
            cleaned = raw[1:-1].encode('utf-8').decode('unicode_escape')
            return json.loads(cleaned)
        raise

if __name__ == "__main__":
    print("Make sure Gmail is open in Chrome and you are logged in.")
    time.sleep(2)
    emails = get_unread_emails(limit=5)
    print(json.dumps(emails, indent=2, ensure_ascii=False))
