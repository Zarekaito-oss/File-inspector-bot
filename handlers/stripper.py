import io
import logging
from pathlib import Path

from aiogram import Router, Bot, F
from aiogram.types import Message, BufferedInputFile

from services.image_stripper import strip_image_metadata
from services.pdf_stripper import strip_pdf_metadata

logger = logging.getLogger(__name__)
router = Router()

MAX_FILE_SIZE = 20 * 1024 * 1024

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".pdf"}


async def _download_file(bot: Bot, file_id: str) -> bytes:
    file = await bot.get_file(file_id)
    buffer = io.BytesIO()
    await bot.download_file(file.file_path, destination=buffer)
    return buffer.getvalue()


async def _process_and_reply(message: Message, bot: Bot, file_id: str, filename: str):
    ext = Path(filename).suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        await message.reply(
            f"\u26a0\ufe0f Unsupported format: <code>{ext or 'unknown'}</code>\n\n"
            "I currently support <b>JPG/JPEG</b> photos and <b>PDF</b> documents."
        )
        return

    status_msg = await message.reply("\U0001f50d Scanning for metadata\u2026")

    try:
        raw_bytes = await _download_file(bot, file_id)

        if len(raw_bytes) > MAX_FILE_SIZE:
            await status_msg.edit_text("\u274c File exceeds the 20 MB limit.")
            return

        if ext in {".jpg", ".jpeg"}:
            clean_bytes, report = strip_image_metadata(raw_bytes)
            label = "photo"
        else:
            clean_bytes, report = strip_pdf_metadata(raw_bytes)
            label = "document"

        stem = Path(filename).stem
        clean_filename = f"{stem}_clean{ext}"

        output_file = BufferedInputFile(clean_bytes, filename=clean_filename)

        if report["fields_removed"] == 0:
            caption = (
                "\u2705 <b>No metadata found</b>\n"
                "This file was already clean. Returning it unchanged."
            )
        else:
            fields = "\n".join(f"  \u2022 {f}" for f in report["removed_fields"])
            caption = (
                f"\U0001f6e1\ufe0f <b>Metadata stripped successfully!</b>\n\n"
                f"<b>Removed {report['fields_removed']} field(s):</b>\n"
                f"{fields}\n\n"
                f"\u2705 Your sanitized {label} is safe to share."
            )

        await status_msg.delete()
        await message.reply_document(output_file, caption=caption)
        logger.info(
            "Processed file '%s' for user %s \u2014 removed %d fields",
            filename,
            message.from_user.id,
            report["fields_removed"],
        )

    except Exception as e:
        logger.exception("Failed to process file '%s': %s", filename, e)
        await status_msg.edit_text(
            "\u274c <b>Processing failed.</b>\n\n"
            "The file may be corrupted or in an unsupported variant. "
            "Please try again or use /help."
        )


@router.message(F.document)
async def handle_document(message: Message, bot: Bot):
    doc = message.document
    await _process_and_reply(message, bot, doc.file_id, doc.file_name or "file.bin")


@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot):
    await message.reply(
        "\U0001f4ce <b>Tip:</b> You sent this as a compressed photo.\n\n"
        "For best results (no quality loss), please resend it using "
        "<i>Attach \u2192 File</i> so I receive the original full-quality image."
    )


@router.message()
async def handle_unknown(message: Message):
    if message.text and not message.text.startswith("/"):
        await message.reply(
            "Send me a <code>.jpg</code> or <code>.pdf</code> file and I'll "
            "strip its metadata. Use /help for more info."
        )
