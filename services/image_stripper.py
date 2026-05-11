import io
from typing import Tuple
from PIL import Image
from PIL.ExifTags import TAGS


FRIENDLY_TAG_NAMES = {v: k for k, v in TAGS.items()}


def _collect_exif_field_names(exif_data: dict) -> list[str]:
    names = []
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, f"Tag_{tag_id}")
        if value is not None:
            names.append(tag_name)
    return names


def strip_image_metadata(raw_bytes: bytes) -> Tuple[bytes, dict]:
    with Image.open(io.BytesIO(raw_bytes)) as img:
        exif_data = img._getexif() or {}
        removed_fields = _collect_exif_field_names(exif_data)

        data = list(img.getdata())
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)

        if img.info.get("icc_profile"):
            clean_img.save_to = lambda buf: clean_img.save(
                buf, format="JPEG", quality=95, icc_profile=img.info["icc_profile"]
            )

        output_buffer = io.BytesIO()
        save_kwargs = {"format": "JPEG", "quality": 95}
        if img.info.get("icc_profile"):
            save_kwargs["icc_profile"] = img.info["icc_profile"]

        clean_img.save(output_buffer, **save_kwargs)

    report = {
        "fields_removed": len(removed_fields),
        "removed_fields": removed_fields,
    }
    return output_buffer.getvalue(), report
