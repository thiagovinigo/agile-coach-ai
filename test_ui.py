from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to localhost:8080...")
        page.goto("http://localhost:8080/index.html")
        page.wait_for_timeout(2000)

        # 1. Click 'Scrumban' main menu
        print("Clicking Scrumban menu...")
        page.click("a[data-target='scrumban-view']")
        page.wait_for_timeout(1000)

        # 2. Inside Scrumban view, find the "O que é" button and click it
        btn_locator = page.locator("#kb-scrumban .kb-nav-btn:has-text('O que é')").first
        if btn_locator.count() > 0:
            print("Clicking 'O que é'...")
            btn_locator.click()
            page.wait_for_timeout(1000)

            # 3. Check for the KCP content
            content_visible = page.is_visible("#kb-scrumban .sub-page:has-text('Visão Especialista KCP')")
            print("KCP Content visible in 'O que é':", content_visible)
            
            # Print a tiny snippet to be absolutely sure
            if content_visible:
                snippet = page.locator("#kb-scrumban .sub-page:has-text('Visão Especialista KCP')").inner_text()
                # Safely print without encode errors
                print("Snippet:", snippet.encode('ascii', 'ignore').decode('ascii')[:300])
        else:
            print("Button 'O que é' not found!")

        browser.close()

if __name__ == "__main__":
    run()
