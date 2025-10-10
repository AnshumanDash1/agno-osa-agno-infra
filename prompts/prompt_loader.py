from pathlib import Path
from textwrap import dedent

# Cache for loaded prompts
_prompts = {}

def load_prompts(folder: str = None):
    """Load all .md files in the given folder into a dict."""
    global _prompts
    if _prompts:
        return _prompts  # already loaded

    folder_path = Path(folder or Path(__file__).parent)
    for file in folder_path.glob("*.md"):
        _prompts[file.stem] = dedent(file.read_text())

    return _prompts


def get_prompt(name: str) -> str:
    """Fetch a specific prompt by name (without .md extension)."""
    if not _prompts:
        load_prompts()
    return _prompts.get(name, f"[Prompt '{name}' not found]")
