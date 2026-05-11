import io
from typing import Tuple
from pypdf import PdfReader, PdfWriter


METADATA_FIELDS = [
    "/Title",
    "/Author",
    "/Subject",
    "/Keywords",
    "/Creator",
    "/Producer",
    "/CreationDate",
    "/ModDate",
    "/Trapped",
    "/PTEX.Fullbanner",
    "/PTEX.FileName",
]


def _collect_present_fields(metadata) -> list[str]:
    if metadata is None:
        return []
    present = []
    for field in METADATA_FIELDS:
        value = metadata.get(field)
        if value:
            label = field.lstrip("/")
            present.append(label)
    for key in metadata:
        if key not in METADATA_FIELDS and metadata.get(key):
            present.append(f"Custom: {key.lstrip('/')}")
    return present


def strip_pdf_metadata(raw_bytes: bytes) -> Tuple[bytes, dict]:
    reader = PdfReader(io.BytesIO(raw_bytes))
    removed_fields = _collect_present_fields(reader.metadata)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata({})

    if writer._info:
        writer._info.get_object().clear()

    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    report = {
        "fields_removed": len(removed_fields),
        "removed_fields": removed_fields,
    }
    return output_buffer.getvalue(), report
