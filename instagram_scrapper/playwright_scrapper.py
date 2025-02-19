import os
import random
import time
import json
import requests
from tqdm import tqdm
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth


def human_delay(a=1, b=3):
    """Introduce random delays to mimic human behavior."""
    time.sleep(random.uniform(a, b))


def save_cookies(context, path="cookies.json"):
    cookies = context.cookies()
    with open(path, "w") as f:
        json.dump(cookies, f)


def load_cookies(context, path="cookies.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        return True
    return False


def download_media(url, folder, filename):
    """🔹 Function to Download Media"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(folder, filename), "wb") as file:
            for chunk in tqdm(response.iter_content(1024), desc=f"Downloading {filename}", unit="KB"):
                file.write(chunk)
    else:
        print(f"❌ Failed to download: {url}")


def download_saved_posts(username, password, folder="saved_posts"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)    # Use non-headless for better stealth
        context = browser.new_context()
        page = context.new_page()

        # Apply stealth to avoid detection
        stealth(page)

        # Try loading existing cookies
        if not load_cookies(context):
            # Navigate to Instagram login
            page.goto("https://www.instagram.com/accounts/login/")
            human_delay(3, 5)

            # Enter username and password
            page.fill('input[name="username"]', username, timeout=10000)
            human_delay()
            page.fill('input[name="password"]', password)
            human_delay()

            # Click login
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")
            human_delay(5, 7)

            # Handle "Save Your Login Info?" popup
            try:
                page.click("//button[contains(text(), 'Not Now')]")
                human_delay()
            except:
                pass

            # Handle "Turn on Notifications" popup
            try:
                page.click("//button[contains(text(), 'Not Now')]")
                human_delay()
            except:
                pass

            # Save cookies after successful login
            save_cookies(context)

        # Go to saved posts
        page.goto(f"https://www.instagram.com/{username}/saved/")
        page.wait_for_load_state("networkidle")
        human_delay(3, 5)

        # Scroll to load saved posts
        last_height = page.evaluate("document.body.scrollHeight")
        for _ in tqdm(range(10), desc="Scrolling through saved posts"):
            page.mouse.wheel(0, last_height)
            human_delay(2, 4)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract post links
        post_links = page.query_selector_all('article a')
        post_urls = [link.get_attribute('href') for link in post_links]

        print(f"Found {len(post_urls)} saved posts.")

        # Create download directory
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Download media from each post
        for idx, post_url in enumerate(tqdm(post_urls, desc="Downloading posts")):
            page.goto(f"https://www.instagram.com{post_url}")
            page.wait_for_load_state("networkidle")
            human_delay(2, 4)

            # Extract image/video URLs
            media_elements = page.query_selector_all('img, video')
            for i, media in enumerate(media_elements):
                media_url = media.get_attribute('src')
                if media_url:
                    extension = 'mp4' if 'video' in media.evaluate('el => el.tagName').lower() else 'jpg'
                    filename = f"post_{idx + 1}_{i + 1}.{extension}"
                    download_media(media_url, folder, filename)

        print("✅ Download completed!")

        browser.close()

if __name__ == "__main__":
    USERNAME = "your_instagram_username"
    PASSWORD = "your_instagram_password"
    download_saved_posts(USERNAME, PASSWORD)
