import os
import typer
from datetime import datetime
from pathlib import Path
from typing import Optional
import pyperclip

app = typer.T.Typer()

RAW_NOTES_DIR = Path("raw_notes")
SUMMARIES_DIR = Path("summaries")

RAW_NOTES_DIR.mkdir(exist_ok=True)
SUMMARIES_DIR.mkdir(exist_ok=True)


def get_timestamp_name() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_to_raw(text: str, name: Optional[str] = None) -> str:
    if name is None:
        name = get_timestamp_name()
    filepath = RAW_NOTES_DIR / f"{name}.txt"
    filepath.write_text(text, encoding="utf-8")
    return str(filepath)


def load_from_raw(name: str) -> str:
    filepath = RAW_NOTES_DIR / f"{name}.txt"
    if not filepath.exists():
        raise FileNotFoundError(f"Raw note not found: {filepath}")
    return filepath.read_text(encoding="utf-8")


def load_from_summaries(name: str) -> str:
    filepath = SUMMARIES_DIR / f"{name}.md"
    if not filepath.exists():
        raise FileNotFoundError(f"Summary not found: {filepath}")
    return filepath.read_text(encoding="utf-8")


def save_summary(text: str, name: Optional[str] = None) -> str:
    if name is None:
        name = get_timestamp_name()
    filepath = SUMMARIES_DIR / f"{name}.md"
    filepath.write_text(text, encoding="utf-8")
    return str(filepath)


@app.command()
def main(
    copy: bool = typer.Option(False, "-c", "--copy", help="Copy from clipboard and save"),
    name: Optional[str] = typer.Option(None, "--name", help="File name (without extension)"),
):
    if copy:
        text = pyperclip.paste()
        if not text:
            typer.echo("Clipboard is empty!", err=True)
            raise typer.Exit(1)

        filepath = save_to_raw(text, name)
        typer.echo(f"Saved to: {filepath}")
    else:
        typer.echo("Please specify an action: -c", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
