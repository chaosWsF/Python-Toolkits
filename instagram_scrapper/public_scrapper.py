import os
import requests
import argparse
from playwright.sync_api import sync_playwright
from tqdm import tqdm


def download_media(url, folder, filename):
    """🔹 Function to Download Media"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, filename)
        with open(file_path, "wb") as f:
            for chunk in tqdm(response.iter_content(1024), desc=f"Downloading {filename}", unit="KB"):
                f.write(chunk)
        print(f"✅ Downloaded: {file_path}")
    else:
        print(f"❌ Failed to download: {url}")


def download_instagram_post(post_url, folder="downloads"):
    """Use Playwright to extract and download media from a public Instagram post."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"🔗 Opening {post_url}")
        page.goto(post_url, timeout=60000)
        page.wait_for_load_state("networkidle")

        # Extract media URLs
        media_elements = page.query_selector_all('article img, article video')
        media_urls = [el.get_attribute('src') for el in media_elements if el.get_attribute('src')]

        if not media_urls:
            print("❌ No media found.")
            return

        print(f"📷 Found {len(media_urls)} media items.")

        # Download each media item
        for idx, media_url in enumerate(media_urls, start=1):
            ext = "mp4" if ".mp4" in media_url else "jpg"
            filename = f"media_{idx}.{ext}"
            download_media(media_url, folder, filename)

        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download media from a public Instagram post.")
    parser.add_argument("post_url", help="Public Instagram post URL")
    parser.add_argument("-o", "--output", default="downloads", help="Output folder for downloaded media")

    args = parser.parse_args()

    download_instagram_post(args.post_url, folder=args.output)
