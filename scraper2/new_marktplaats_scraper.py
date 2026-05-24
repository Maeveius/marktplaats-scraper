from playwright.sync_api import sync_playwright, Playwright

def marktplaats_scraper(search):
    chromium = playwright.chromium
    browser = chromium.launch(
        headless=False
    )
    page = browser.new_page()
    page.goto("https://www.marktplaats.nl/q/hamtaro+dvd")

    price = page.locator("li.hz-Listing-price").inner_text()
    print(price)


    browser.close()

with sync_playwright() as playwright:
    marktplaats_scraper(playwright)