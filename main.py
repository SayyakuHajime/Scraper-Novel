import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def setup_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome WebDriver initialized.")
    return driver

def save_chapter(chapter_title, content, index, output_dir):
    if not content:
        return False
    
    # Clean filename
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', chapter_title)
    filename = f"Chapter_{index:03d}_{safe_title[:50]}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Chapter {index}: {chapter_title}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content)
    
    print(f"  ✓ Saved: {filename}")
    return True

def scrape_bilibili_novel(url, max_chapters=None, headless=True, output_dir="output"):
    driver = setup_driver(headless=headless)
    
    try:
        print(f"Loading: {url}")
        driver.get(url)
        time.sleep(5)
        
        # Get novel title
        novel_title = "Bilibili_Novel"
        try:
            title_xpath = "/html/body/div[2]/div[2]/div/div[1]/div[2]/div[1]"
            title_elem = driver.find_element(By.XPATH, title_xpath)
            novel_title = title_elem.text.strip()
            print(f"Novel: {novel_title}")
        except:
            print("Could not find novel title, using default")
        
        # Find chapters
        title_elements = driver.find_elements(By.CSS_SELECTOR, "div.title-text")
        total_chapters = len(title_elements)
        print(f"Found {total_chapters} chapters")
        
        if not title_elements:
            print("No chapters found!")
            return
        
        # Limit chapters if specified
        if max_chapters:
            title_elements = title_elements[:max_chapters]
            print(f"Processing first {len(title_elements)} chapters")
        
        # Create output directory
        safe_novel_title = re.sub(r'[<>:"/\\|?*]', '_', novel_title)
        novel_dir = os.path.join(output_dir, safe_novel_title)
        os.makedirs(novel_dir, exist_ok=True)
        print(f"Output directory: {novel_dir}")
        
        success_count = 0
        
        # Process chapters
        for i, elem in enumerate(title_elements, 1):
            chapter_title = elem.text.strip()
            print(f"\n[{i}/{len(title_elements)}] {chapter_title}")
            
            # Store original tab
            original_window = driver.current_window_handle
            
            try:
                # Click chapter (opens new tab)
                driver.execute_script("arguments[0].click();", elem)
                time.sleep(3)
                
                # Check for new tab
                new_windows = driver.window_handles
                if len(new_windows) > 1:
                    # Switch to new tab
                    new_tab = [w for w in new_windows if w != original_window][0]
                    driver.switch_to.window(new_tab)
                    
                    # Extract content
                    try:
                        content_xpath = "/html/body/div[2]/div[4]/div[1]/div[4]"
                        content_div = driver.find_element(By.XPATH, content_xpath)
                        paragraphs = content_div.find_elements(By.TAG_NAME, "p")
                        
                        # Extract text from paragraphs
                        content_parts = []
                        for p in paragraphs:
                            # Try spans first, then direct text
                            spans = p.find_elements(By.TAG_NAME, "span")
                            if spans:
                                text = " ".join([s.text.strip() for s in spans if s.text.strip()])
                            else:
                                text = p.text.strip()
                            
                            if text and len(text) > 5:  # Skip very short texts
                                content_parts.append(text)
                        
                        if content_parts:
                            full_content = "\n\n".join(content_parts)
                            print(f"  Extracted {len(paragraphs)} paragraphs, {len(full_content)} characters")
                            
                            # Save chapter
                            if save_chapter(chapter_title, full_content, i, novel_dir):
                                success_count += 1
                        else:
                            print("  ✗ No content extracted")
                    
                    except Exception as e:
                        print(f"  ✗ Error extracting content: {e}")
                    
                    # Close tab and return
                    driver.close()
                    driver.switch_to.window(original_window)
                else:
                    print("  ✗ No new tab opened")
            
            except Exception as e:
                print(f"  ✗ Error processing chapter: {e}")
            
            # Respectful delay
            time.sleep(2)
        
        print(f"\n✅ Completed! {success_count}/{len(title_elements)} chapters saved")
        print(f"📁 Files saved in: {novel_dir}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🎭 Bilibili Novel Scraper")
    print("=" * 40)
    
    url = input("Enter Bilibili novel URL: ").strip()
    if not url:
        print("❌ No URL provided")
        exit()
    
    try:
        max_chapters = int(input("Max chapters to scrape (0 for all): ") or "0")
        if max_chapters <= 0:
            max_chapters = None
    except:
        max_chapters = 5
        print(f"Using default: {max_chapters} chapters")
    
    headless_input = input("Headless mode? (y/n, default: n): ").strip().lower()
    headless = headless_input == 'y'
    
    print(f"\n🚀 Starting scraper (headless: {headless})...")
    scrape_bilibili_novel(url, max_chapters=max_chapters, headless=headless)