from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentChunk:
    destination: str
    title: str
    content: str
    source: str
    chunk_index: int


def _build_chunks(
    text: str,
    destination: str,
    title: str,
    source: str,
) -> list[DocumentChunk]:
    """
    Split a Markdown document into heading-based chunks.

    Level-one headings are treated as document metadata.
    Level-two headings start individual knowledge sections.
    """

    sections: list[tuple[str, list[str]]] = []

    current_title: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("## "):
            if current_title is not None and current_lines:
                sections.append(
                    (
                        current_title,
                        current_lines,
                    )
                )

            current_title = stripped[3:].strip()
            current_lines = []

            continue

        if stripped.startswith("# "):
            continue

        if current_title is not None:
            current_lines.append(stripped)

    if current_title is not None and current_lines:
        sections.append(
            (
                current_title,
                current_lines,
            )
        )

    chunks: list[DocumentChunk] = []

    for index, (section_title, lines) in enumerate(
        sections
    ):
        content = "\n".join(lines).strip()

        if not content:
            continue

        chunks.append(
            DocumentChunk(
                destination=destination,
                title=section_title,
                content=content,
                source=source,
                chunk_index=index,
            )
        )

    return chunks


def chunk_markdown_file(
    file_path: str | Path,
    destination: str,
) -> list[DocumentChunk]:
    """
    Read a Markdown destination document and convert it
    into structured knowledge chunks.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge document not found: {path}"
        )

    if path.suffix.lower() != ".md":
        raise ValueError(
            f"Unsupported document type: {path.suffix}"
        )

    text = path.read_text(
        encoding="utf-8-sig",
    )

    return _build_chunks(
        text=text,
        destination=destination,
        title=path.stem,
        source=str(path),
    )