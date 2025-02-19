import os
import time
import requests
from tqdm import tqdm
from playwright.sync_api import sync_playwright

# 🔹 Your Instagram Credentials
USERNAME = "your_username"
PASSWORD = "your_password"

# 🔹 Folder to Save Media
SAVE_FOLDER = "Instagram_Saved"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# 🔹 Function to Download Media
def download_file(url, folder, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(folder, filename), "wb") as file:
            for chunk in tqdm(response.iter_content(1024), desc=f"Downloading {filename}", unit="KB"):
                file.write(chunk)
    else:
        print(f"❌ Failed to download: {url}")

# 🔹 Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True to run without UI
    context = browser.new_context()
    page = context.new_page()

    # 🔹 Open Instagram Login Page
    page.goto("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    # 🔹 Log In to Instagram
    page.fill("input[name='username']", USERNAME)
    page.fill("input[name='password']", PASSWORD)
    page.press("input[name='password']", "Enter")
    time.sleep(10)

    # 🔹 Navigate to Saved Posts
    page.goto(f"https://www.instagram.com/{USERNAME}/saved/")
    time.sleep(5)

    # 🔹 Scroll to Load More Posts
    POST_LIMIT = 50  # Adjust based on number of saved posts
    last_height = page.evaluate("document.body.scrollHeight")

    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height or len(page.locator("article a").all()) >= POST_LIMIT:
            break
        last_height = new_height

    # 🔹 Extract Post URLs
    post_links = [a.get_attribute("href") for a in page.locator("article a").all()]
    print(f"🔹 Found {len(post_links)} saved posts.")

    # 🔹 Visit Each Post and Download All Media
    for index, post_url in enumerate(post_links):
        page.goto(post_url)
        time.sleep(5)

        media_count = 0

        while True:
            media_count += 1

            # Download Images
            images = page.locator("article img").all()
            for img in images:
                img_url = img.get_attribute("src")
                filename = f"post_{index + 1}_image_{media_count}.jpg"
                download_file(img_url, SAVE_FOLDER, filename)

            # Download Videos
            videos = page.locator("article video").all()
            for vid in videos:
                vid_url = vid.get_attribute("src")
                filename = f"post_{index + 1}_video_{media_count}.mp4"
                download_file(vid_url, SAVE_FOLDER, filename)

            # Check for "Next" button in carousel
            if page.locator("button[aria-label='Next']").count() > 0:
                page.click("button[aria-label='Next']")
                time.sleep(3)
            else:
                break  # No more media in carousel

    print("✅ All saved posts downloaded!")
    browser.close()
