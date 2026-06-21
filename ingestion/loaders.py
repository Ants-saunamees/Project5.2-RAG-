from pathlib import Path

def loader(department: str):
    base_path = Path(__file__).resolve().parent.parent
    folder = base_path / "docs" / department

    for path in folder.rglob("*.md"):
        text = path.read_text(encoding="utf-8")

        yield {
            "text": text,
            "metadata": {
                "department": department,
                "source": str(path)
            }
        }

