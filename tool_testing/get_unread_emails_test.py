import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from computer_use_tool import list_recent_emails, open_chrome_url, read_email_body

if __name__ == "__main__":
    try:
        print("Opening Gmail in Chrome...")
        open_chrome_url("https://mail.google.com/")
    except RuntimeError as exc:
        print(f"Failed to open Gmail: {exc}")
        sys.exit(1)

    print("Waiting for Gmail to settle...")
    time.sleep(3)

    try:
        emails = list_recent_emails(limit=5)
    except RuntimeError as exc:
        print("Could not retrieve message list:")
        print(f"  {exc}")
        if "Chrome is blocking" in str(exc):
            print("\nEnable Chrome > View > Developer > Allow JavaScript from Apple Events and re-run.")
        sys.exit(1)

    print("Recent messages:")
    print(json.dumps(emails, indent=2, ensure_ascii=False))

    if emails:
        chosen = emails[0]["thread_id"]
        print(f"\nFetching body for first thread: {chosen}")
        try:
            details = read_email_body(thread_id=chosen)
        except RuntimeError as exc:
            print("Could not open the selected thread:")
            print(f"  {exc}")
            sys.exit(1)
        print(json.dumps(details, indent=2, ensure_ascii=False))
    else:
        print("No messages returned. Ensure Gmail inbox is visible in Chrome.")
