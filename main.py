import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BilibiliNovelScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome WebDriver."""
        self.driver = None
        self.wait = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Set up Chrome WebDriver with options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("Chrome WebDriver initialized successfully.")
        except Exception as e:
            print(f"Error initializing Chrome WebDriver: {e}")
            print("Please make sure ChromeDriver is installed and in PATH.")
            raise
    
    def extract_chapters(self, url):
        """Extract chapter list from the novel page."""
        print(f"Loading novel page: {url}")
        self.driver.get(url)
        time.sleep(3)
        
        # Get novel title
        try:
            title_element = self.driver.find_element(By.TAG_NAME, "h1")
            novel_title = title_element.text.strip() or "Unknown Novel"
        except:
            novel_title = "Unknown Novel"
        
        print(f"Found novel: {novel_title}")
        
        # Find chapters using XPath from README
        chapters = []
        chapter_index = 1
        
        while True:
            try:
                if chapter_index == 1:
                    xpath = "/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[1]"
                else:
                    xpath = f"/html/body/div[2]/div[2]/div/div[2]/div/div[{chapter_index}]/div[2]/div[1]/div[1]"
                
                chapter_element = self.driver.find_element(By.XPATH, xpath)
                chapter_title = chapter_element.text.strip()
                chapter_link = chapter_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                if chapter_title and chapter_link:
                    chapters.append({
                        'title': chapter_title,
                        'url': chapter_link,
                        'index': chapter_index
                    })
                    print(f"Chapter {chapter_index}: {chapter_title}")
                
                chapter_index += 1
                
            except NoSuchElementException:
                break
            except Exception as e:
                print(f"Error finding chapter {chapter_index}: {e}")
                break
        
        print(f"Found {len(chapters)} chapters total")
        return novel_title, chapters
    
    def scrape_chapter(self, chapter_url):
        """Scrape content from a single chapter."""
        try:
            self.driver.get(chapter_url)
            time.sleep(2)
            
            # Use XPath from README specification
            content_xpath = "/html/body/div[2]/div[4]/div[1]/div[4]"
            content_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, content_xpath))
            )
            
            # Extract paragraphs
            paragraphs = []
            paragraph_index = 1
            
            while True:
                try:
                    paragraph_xpath = f"{content_xpath}/p[{paragraph_index}]"
                    paragraph_element = self.driver.find_element(By.XPATH, paragraph_xpath)
                    text = paragraph_element.text.strip()
                    if text:
                        paragraphs.append(text)
                    paragraph_index += 1
                except NoSuchElementException:
                    break
            
            # Fallback: get all text if no paragraphs found
            if not paragraphs:
                content_text = content_element.text.strip()
                if content_text:
                    paragraphs = [p.strip() for p in content_text.split('\n\n') if p.strip()]
            
            return '\n\n'.join(paragraphs) if paragraphs else None
            
        except Exception as e:
            print(f"Error scraping chapter: {e}")
            return None
    
    def save_chapter(self, title, content, index, output_dir):
        """Save chapter to text file."""
        if not content:
            return False
        
        # Clean filename
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        filename = f"Chapter_{index:03d}_{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Chapter {index}: {title}\n")
                f.write("=" * 50 + "\n\n")
                f.write(content)
            print(f"Saved: {filename}")
            return True
        except Exception as e:
            print(f"Error saving {title}: {e}")
            return False
    
    def scrape_novel(self, novel_url, output_dir="output"):
        """Main scraping method."""
        # Validate URL
        if "bilibili.com/read/readlist/" not in novel_url:
            print("Invalid URL format. Use: https://www.bilibili.com/read/readlist/...")
            return False
        
        try:
            # Extract chapters
            novel_title, chapters = self.extract_chapters(novel_url)
            
            if not chapters:
                print("No chapters found.")
                return False
            
            # Create output directory
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', novel_title)
            novel_dir = os.path.join(output_dir, safe_title)
            os.makedirs(novel_dir, exist_ok=True)
            
            print(f"\nStarting to scrape {len(chapters)} chapters...")
            print(f"Output: {novel_dir}")
            
            # Scrape each chapter
            success_count = 0
            for i, chapter in enumerate(chapters, 1):
                print(f"\n[{i}/{len(chapters)}] Processing: {chapter['title']}")
                
                content = self.scrape_chapter(chapter['url'])
                if content and self.save_chapter(chapter['title'], content, chapter['index'], novel_dir):
                    success_count += 1
                else:
                    print(f"Failed to scrape: {chapter['title']}")
                
                # Be respectful - add delay
                time.sleep(1)
            
            print(f"\nCompleted! {success_count}/{len(chapters)} chapters saved to: {novel_dir}")
            return True
            
        except Exception as e:
            print(f"Scraping error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed.")


def main():
    print("Bilibili Novel Scraper")
    print("=" * 30)
    
    # Get URL
    novel_url = input("Enter Bilibili novel URL: ").strip()
    if not novel_url:
        print("No URL provided.")
        return
    
    # Get output directory
    output_dir = input("Output directory (default: 'output'): ").strip() or "output"
    
    # Headless mode
    headless = input("Headless mode? (y/n, default: y): ").strip().lower() != 'n'
    
    try:
        scraper = BilibiliNovelScraper(headless=headless)
        scraper.scrape_novel(novel_url, output_dir)
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure ChromeDriver is installed:")
        print("   https://chromedriver.chromium.org/")


if __name__ == "__main__":
    main()
