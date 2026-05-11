from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

WELCOME_TEXT = (
    "\U0001f6e1\ufe0f <b>Metadata Stripper \u2014 Privacy Converter</b>\n\n"
    "I silently erase hidden data from your files before you share them publicly.\n\n"
    "<b>What I strip:</b>\n"
    "\U0001f4f7 <b>JPG/JPEG photos</b> \u2014 GPS coordinates, camera model, lens info, "
    "creation timestamps, author tags, software fingerprints\n"
    "\U0001f4c4 <b>PDF documents</b> \u2014 Author name, organization, creation/modification "
    "dates, software used, custom properties\n\n"
    "<b>How to use:</b>\n"
    "Simply send or forward any <code>.jpg</code> or <code>.pdf</code> file.\n"
    "I'll return a clean, sanitized copy \u2014 identical content, zero metadata.\n\n"
    "\u26a1 All processing happens locally. Your files are never stored."
)

HELP_TEXT = (
    "\U0001f4cb <b>Supported file types:</b>\n"
    "\u2022 <code>.jpg</code> / <code>.jpeg</code> \u2014 EXIF data removed via Pillow\n"
    "\u2022 <code>.pdf</code> \u2014 Document metadata cleared via pypdf\n\n"
    "\U0001f4cc <b>Tips:</b>\n"
    "\u2022 For photos, send as a <b>file/document</b> (not compressed image) "
    "to preserve the original resolution.\n"
    "\u2022 Telegram compresses photos sent normally \u2014 use <i>Attach \u2192 File</i> instead.\n\n"
    "\u26a0\ufe0f <b>Limitations:</b>\n"
    "\u2022 Max file size: 20 MB (Telegram Bot API limit)\n"
    "\u2022 Only JPG and PDF formats are supported currently"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT)
