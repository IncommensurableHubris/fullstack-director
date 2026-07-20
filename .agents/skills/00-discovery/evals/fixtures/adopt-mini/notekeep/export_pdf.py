"""PDF export of notes.

NOTE: this module is not wired into the CLI (there is no `export` subcommand in cli.py) and nothing imports it.
It was a spike for a v0.1 idea that was never shipped and is not mentioned in the README. Left in the tree.
"""
from . import store


def export_to_pdf(path: str) -> None:
    """Write all notes to a minimal single-page PDF at `path`."""
    lines = [f"{n['id']}. {n['text']}" for n in store.all_notes()]
    body = "\\n".join(lines) or "(no notes)"
    stream = f"BT /F1 12 Tf 72 720 Td ({body}) Tj ET"
    pdf = (
        "%PDF-1.4\n"
        "1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        "2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        "3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R"
        "/Resources<</Font<</F1 5 0 R>>>>>>endobj\n"
        f"4 0 obj<</Length {len(stream)}>>stream\n{stream}\nendstream endobj\n"
        "5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n"
        "trailer<</Root 1 0 R>>\n%%EOF"
    )
    with open(path, "w", encoding="latin-1") as handle:
        handle.write(pdf)
