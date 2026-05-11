<div align="center">

<br>

```
 _____ _ _        ___                           _             
|  ___(_) | ___  |_ _|_ __  ___ _ __   ___  ___| |_ ___  _ __ 
| |_  | | |/ _ \  | || '_ \/ __| '_ \ / _ \/ __| __/ _ \| '__|
|  _| | | |  __/  | || | | \__ \ |_) |  __/ (__| || (_) | |   
|_|   |_|_|\___| |___|_| |_|___/ .__/ \___|\___|\__\___/|_|   
                                |_|                            
```

**Strip hidden metadata from files — right inside Telegram.**

[![Python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Aiogram](https://img.shields.io/badge/aiogram-3.7-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://aiogram.dev)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](LICENSE)

<br>

---

</div>

## What is this?

A Telegram bot that **silently erases hidden metadata** from your files before you share them publicly.

Every photo and document you create carries invisible fingerprints — GPS coordinates, device info, author names, timestamps. This bot strips all of it.

<br>

## Supported formats

| Format | What gets removed |
|:---|:---|
| **JPG / JPEG** | EXIF data — GPS coords, camera model, lens info, timestamps, software tags |
| **PDF** | Author, organization, creation/modification dates, producer software, custom props |

<br>

## Project structure

```
.
├── main.py                  # Entry point — bot initialization
├── handlers/
│   ├── general.py           # /start and /help commands
│   └── stripper.py          # File processing router
├── services/
│   ├── image_stripper.py    # EXIF removal via Pillow
│   └── pdf_stripper.py      # PDF metadata wipe via pypdf
├── requirements.txt
└── .env.example
```

<br>

## Quick start

**1 · Clone**
```bash
git clone https://github.com/Zarekaito-oss/File-inspector-bot.git
cd File-inspector-bot
```

**2 · Environment**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3 · Configure**
```bash
cp .env.example .env
# Add your bot token from @BotFather
```

**4 · Run**
```bash
python main.py
```

<br>

## How it works

```
User sends file  →  Bot downloads  →  Metadata scanned & stripped  →  Clean file returned
                                          ↓
                                    Removal report shown
                                    (fields found & erased)
```

- **Photos** are reconstructed pixel-by-pixel (no EXIF survives)
- **PDFs** get all info dictionary entries wiped
- Files are **never stored** — processed in memory and discarded

<br>

## Bot commands

| Command | Description |
|:---|:---|
| `/start` | Welcome message + feature overview |
| `/help` | Supported formats, tips, and limits |

> **Tip:** Send photos as *files* (not compressed images) for full-quality processing.

<br>

## Requirements

- Python 3.10+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

| Package | Purpose |
|:---|:---|
| `aiogram 3.7` | Async Telegram Bot framework |
| `Pillow 10.3` | Image processing & EXIF removal |
| `pypdf 4.2` | PDF metadata manipulation |
| `python-dotenv` | Environment variable loading |

<br>

## Limitations

- Max file size: **20 MB** (Telegram Bot API limit)
- Only **JPG/JPEG** and **PDF** formats supported
- Telegram-compressed photos lose quality before reaching the bot

<br>

<div align="center">

---

<sub>Built for privacy. No data stored. No logs kept. Just clean files.</sub>

</div>
