from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


def test_instagram_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--ignore-certificate-errors'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            ignore_https_errors=True,
            java_script_enabled=True
        )
        page = context.new_page()

        # Apply stealth
        stealth_sync(page)

        # Go to Instagram login
        page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
        page.wait_for_load_state("networkidle")

        # Wait to visually confirm the page loaded
        page.wait_for_selector('input[name="username"]', timeout=15000)
        print("✅ Instagram login page loaded successfully!")

        browser.close()

if __name__ == "__main__":
    test_instagram_login()
