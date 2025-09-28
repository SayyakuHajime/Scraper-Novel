# Scraper-Novel

A Python tool to scrape and translate novel content from Bilibili for personal use.

## Prerequisites
- Python 3.13+
- [UV](https://docs.astral.sh/uv/) package manager
- Google Chrome browser

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Scrape a novel:**
   ```bash
   uv run python main.py
   ```
   Enter a Bilibili readlist URL like: `https://www.bilibili.com/read/readlist/[replace this]`

3. **Translate chapters (optional):**
   ```bash
   uv run python translator.py
   ```
   Requires DeepSeek API key for translation.

## Features

- **Novel Scraping**: Extract all chapters from Bilibili readlists
- **Translation**: Translate Chinese novels to multiple languages (Not Implemented Yet)
- **Clean Output**: Organized text files with proper formatting
- **Progress Tracking**: Real-time progress updates
- **Error Handling**: Robust error recovery

## Output Structure
```
output/
└── [Novel Title]/
    ├── Chapter_001_[Title].txt
    ├── Chapter_002_[Title].txt
    └── ...

```

## Important Notice

**For personal use only.** Respect Bilibili's Terms of Service and copyright laws.
