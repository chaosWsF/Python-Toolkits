from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


def test_instagram_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--ignore-certificate-errors'])
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
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
