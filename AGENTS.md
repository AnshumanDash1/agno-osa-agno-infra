# Repository Guidelines

## Project Structure & Module Organization
The automation entry point lives in `my_os.py`, which wires Agno agents, tools, and serving configuration. Browser automation helpers are in `computer_use_tool.py`. Scenario scripts and manual tests sit under `tool_testing/`; keep exploratory utilities there so production code stays clean. The `agno-infra-venv/` directory is a managed Python virtual environment—replace it locally rather than committing changes inside.

## Build, Test, and Development Commands
Use the repo’s virtualenv: `source agno-infra-venv/bin/activate`. Run the agent locally with `python my_os.py`; it serves the AgentOS app on port 7777 with hot reload. To validate the Gmail tools, execute `python tool_testing/get_unread_emails_test.py` while Chrome is open to Gmail and "Allow JavaScript from Apple Events" is enabled (Chrome > View > Developer). When adding tooling, prefer `python -m <module>` invocations so scripts resolve package-relative imports.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation and descriptive snake_case for functions, variables, and files. Keep class names in PascalCase and constants in ALL_CAPS. Type hints are expected on all public functions, mirroring existing modules. Use docstrings sparingly to explain browser automation pitfalls or non-obvious AgentOS configuration. Escape backslashes and quotes explicitly when embedding JavaScript or AppleScript in strings.

## Testing Guidelines
Current tests are manual harnesses under `tool_testing/`. Mirror that pattern for new browser flows: accept dependencies on Chrome state, print structured JSON, and guard against missing windows. When feasible, isolate pure Python helpers and cover them with `pytest` (add to `requirements.txt` if introduced). Before opening a PR, run the relevant test scripts and document any environment prerequisites (e.g., Chrome profile, Gmail access, enabled developer setting).

Use the Playwright MCP harness to exercise AgentOS application flows end-to-end and catch regressions before shipping changes.
Whenever you are testing, go to https://os.agno.com/chat?type=agent&id=assistant&session=66beddc6-589c-441a-9bf3-35ce5bf1612b to chat with the deployed bot and make sure all is well.

## Commit & Pull Request Guidelines
Write imperative, 60-character-or-shorter commit subjects (example: `Add Gmail unread scraping utility`). Group related changes per commit and add concise bodies when behavior changes. PRs should summarize the intent, list test commands executed, and link any tracking issues. Include screenshots or logs when demonstrating UI automation results and call out security-sensitive configuration changes, especially API keys or OAuth scopes.

## Agent & Security Notes
Store model keys in `.env`; never check credentials into git. Confirm Chrome automation only targets domains required for the scenario, and sanitize logged output before sharing. Register new agents or tools in `my_os.py` and document required permissions in the PR description, including Gmail access expectations.
