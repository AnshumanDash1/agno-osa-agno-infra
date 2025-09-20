"""Local file system helpers."""
from pathlib import Path
from typing import Dict, List

from agno.tools import Toolkit

from tools.common import not_implemented


def fs_open_file(path: str) -> Dict[str, str]:
    """Open a local file (placeholder until automation is wired)."""
    if not path:
        raise ValueError("path is required")
    return not_implemented(
        feature="fs_open_file",
        integration_hint="Use macOS 'open' command or platform-specific automation to launch files.",
    )


def fs_read_text(path: str, limit: int = 5000) -> Dict[str, str]:
    """Read text content from a local file."""
    if not path:
        raise ValueError("path is required")
    file_path = Path(path).expanduser()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise ValueError("path must point to a file")

    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        content = handle.read(limit)
    truncated = len(content) == limit
    return {
        "status": "ok",
        "path": str(file_path),
        "content": content,
        "truncated": truncated,
    }


def fs_search_by_name(pattern: str, base_dir: str = "~", max_results: int = 20) -> Dict[str, List[str]]:
    """Search for files by name pattern under a base directory."""
    if not pattern:
        raise ValueError("pattern is required")
    root = Path(base_dir).expanduser()
    if not root.exists():
        raise FileNotFoundError(f"Base directory not found: {root}")
    matches: List[str] = []
    for path in root.rglob(pattern):
        matches.append(str(path))
        if len(matches) >= max_results:
            break
    return {"results": matches, "count": len(matches)}


def fs_read_pdf(path: str) -> Dict[str, str]:
    """Read text from a PDF (placeholder for OCR integration)."""
    if not path:
        raise ValueError("path is required")
    return not_implemented(
        feature="fs_read_pdf",
        integration_hint=(
            "Integrate with pdfminer or OCR (e.g., Tesseract) to extract text and relay aloud."
        ),
    )


class FileSystemToolkit(Toolkit):
    """Toolkit offering local file utilities."""

    def __init__(self) -> None:
        super().__init__(name="file_system")
        self.register(fs_open_file)
        self.register(fs_read_text)
        self.register(fs_search_by_name)
        self.register(fs_read_pdf)

    def instructions(self) -> str:
        return "File system tools provide quick inspection helpers and call out OCR requirements for PDFs."


FILE_SYSTEM_TOOLKIT = FileSystemToolkit()

__all__ = [
    "FILE_SYSTEM_TOOLKIT",
    "FileSystemToolkit",
]
