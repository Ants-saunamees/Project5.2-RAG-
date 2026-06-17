from pathlib import Path

def loader(department: str):
    print("loader hit")
    base_path = Path(__file__).resolve().parent.parent
    folder = base_path / "docs" / department
    print("folder hit")
    print("Looking in:", folder.absolute())

    for path in folder.rglob("*.md"):
        print("Found file:", path)

        text = path.read_text(encoding="utf-8")

        yield {
            "text": text,
            "metadata": {
                "department": department,
                "source": str(path)
            }
        }

