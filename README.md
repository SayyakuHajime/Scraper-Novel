# Scraper-Novel

A simple Python tool to scrape novel content from the Bilibili website for personal use. Clean, functional, and easy to use.

### Prerequisites
- Python 3.13+ 
- [UV](https://docs.astral.sh/uv/) package manager
- Google Chrome browser
- ChromeDriver ([Download here](https://chromedriver.chromium.org/))

### Installation & Usage

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the scraper:**
   ```bash
   uv run main.py
   ```

3. **Follow the prompts:**
   - Enter your Bilibili novel URL
   - Choose output directory 
   - Select headless mode

## How It Works

1. **Input**: Provide a Bilibili novel readlist URL:
   ```
   https://www.bilibili.com/read/readlist/rl123456
   ```

2. **Chapter Discovery**: Finds all chapters using XPath selectors
   
3. **Content Extraction**: Scrapes each chapter's text content

4. **Output**: Saves chapters as `.txt` files:
   ```
   output/
   └── [Novel Title]/
       ├── Chapter_001_[Chapter Title].txt
       ├── Chapter_002_[Chapter Title].txt
       └── ...
   ```

## Features

- Simple command-line interface
- Automatic chapter detection  
- Clean text extraction
- UTF-8 encoding support
- Headless browser option
- Progress tracking
- Error handling

## Troubleshooting

**ChromeDriver not found?**
1. Download from [ChromeDriver](https://chromedriver.chromium.org/)
2. Add to your PATH environment variable

**Can't see what's happening?**
- Choose 'n' for headless mode when prompted
- This opens a visible browser window

**No chapters found?**
- Verify the URL is a Bilibili readlist URL
- Check your internet connection
- Try again later (site may be temporarily unavailable)

## Important Notice

> **For personal use only**. Please respect Bilibili's Terms of Service and copyright laws. Support authors through official channels when possible.
