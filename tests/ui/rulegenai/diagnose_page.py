"""
Diagnostic script to explore RuleGen AI page structure
"""

import os
import sys

workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from playwright.sync_api import sync_playwright


def diagnose_rulegenai():
    """Explore the RuleGen AI application structure"""

    base_url = "http://rule-gen-ai.dev.bci.aws.cudaops.com"
    username = os.environ.get("RULEGENAI_USERNAME", "")
    password = os.environ.get("RULEGENAI_PASSWORD", "")

    if not username or not password:
        raise ValueError("RULEGENAI_USERNAME and RULEGENAI_PASSWORD environment variables must be set")

    screenshots_dir = os.path.join(workspace_root, "screenshots", "rulegenai", "diagnostic")
    os.makedirs(screenshots_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible browser for debugging
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        print("=" * 60)
        print("RULEGENAI DIAGNOSTIC REPORT")
        print("=" * 60)

        # Step 1: Login
        print("\n[1] Navigating to login page...")
        page.goto(f"{base_url}/login", wait_until="networkidle", timeout=60000)
        page.screenshot(path=f"{screenshots_dir}/01_login_page.png", full_page=True)
        print(f"    URL: {page.url}")

        # Fill login
        print("\n[2] Logging in...")
        page.locator("#username, input[name='username']").first.fill(username)
        page.locator("#password, input[type='password']").first.fill(password)
        page.locator("button[type='submit']").first.click()
        page.wait_for_timeout(3000)
        page.wait_for_load_state("networkidle")
        page.screenshot(path=f"{screenshots_dir}/02_after_login.png", full_page=True)
        print(f"    URL after login: {page.url}")

        # Step 2: Navigate to workspace 12
        print("\n[3] Navigating to workspace 12...")
        page.goto(f"{base_url}/workspaces/12", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)
        page.screenshot(path=f"{screenshots_dir}/03_workspace_12.png", full_page=True)
        print(f"    URL: {page.url}")
        print(f"    Title: {page.title()}")

        # Step 3: Find all navigation links
        print("\n[4] Finding all navigation links...")
        nav_links = page.locator("a[href], button").all()
        print(f"    Found {len(nav_links)} clickable elements")

        links_info = []
        for i, link in enumerate(nav_links[:30]):  # First 30 elements
            try:
                href = link.get_attribute("href") or ""
                text = link.text_content().strip()[:50] if link.text_content() else ""
                tag = link.evaluate("el => el.tagName")
                if text or href:
                    links_info.append({"index": i, "tag": tag, "text": text, "href": href})
            except:
                pass

        print("\n    Navigation elements found:")
        for info in links_info:
            print(f"      [{info['index']}] <{info['tag']}> '{info['text']}' -> {info['href']}")

        # Step 4: Look for rule generator related elements
        print("\n[5] Searching for rule generator elements...")

        search_terms = [
            ("Generate", "button:has-text('Generate'), a:has-text('Generate')"),
            ("New Rule", "button:has-text('New'), a:has-text('New')"),
            ("Create", "button:has-text('Create'), a:has-text('Create')"),
            ("Prompt/Input", "textarea, input[type='text']"),
            ("Rules nav", "a[href*='rule'], a:has-text('Rule')"),
        ]

        for name, selector in search_terms:
            elements = page.locator(selector)
            count = elements.count()
            print(f"    {name}: {count} elements found")
            if count > 0:
                for i in range(min(count, 3)):
                    el = elements.nth(i)
                    text = el.text_content().strip()[:30] if el.text_content() else ""
                    href = el.get_attribute("href") or ""
                    print(f"      - '{text}' {href}")

        # Step 5: Try common rule generator URLs
        print("\n[6] Testing potential rule generator URLs...")
        test_urls = [
            f"{base_url}/workspaces/12/generate",
            f"{base_url}/workspaces/12/rules/new",
            f"{base_url}/workspaces/12/rules/create",
            f"{base_url}/generate",
            f"{base_url}/rules/new",
            f"{base_url}/workspaces/12/rule-generator",
        ]

        for url in test_urls:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=10000)
                page.wait_for_timeout(1000)

                # Check if page loaded successfully (not 404)
                is_404 = page.locator("text=404, text=Not Found, text=Page not found").count() > 0
                has_textarea = page.locator("textarea").count() > 0
                has_generate_btn = page.locator("button:has-text('Generate')").count() > 0

                status = "✓ FOUND GENERATOR!" if (has_textarea or has_generate_btn) else ("✗ 404" if is_404 else "? No generator elements")
                print(f"    {url}")
                print(f"      {status} (textarea: {has_textarea}, generate btn: {has_generate_btn})")

                if has_textarea or has_generate_btn:
                    safe_name = url.replace(base_url, "").replace("/", "_")
                    page.screenshot(path=f"{screenshots_dir}/found_generator{safe_name}.png", full_page=True)

            except Exception as e:
                print(f"    {url} -> Error: {str(e)[:50]}")

        # Step 6: Go back to workspace and click on any "Generate" or "New" buttons
        print("\n[7] Looking for buttons to click on workspace page...")
        page.goto(f"{base_url}/workspaces/12", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)

        # Find and click potential generator buttons
        potential_buttons = [
            "button:has-text('Generate')",
            "button:has-text('New Rule')",
            "button:has-text('Create Rule')",
            "a:has-text('Generate')",
            "a:has-text('New Rule')",
            "[data-testid*='generate']",
            ".generate-btn",
            "#generate-rule",
        ]

        for selector in potential_buttons:
            btn = page.locator(selector)
            if btn.count() > 0:
                print(f"    Found: {selector}")
                try:
                    btn.first.click()
                    page.wait_for_timeout(2000)
                    page.screenshot(path=f"{screenshots_dir}/after_click_{selector.replace(':', '_').replace(' ', '_')[:20]}.png", full_page=True)
                    print(f"      Clicked! New URL: {page.url}")

                    # Check if we found the generator
                    if page.locator("textarea").count() > 0:
                        print("      ✓ FOUND TEXTAREA - This is likely the rule generator!")
                        page.screenshot(path=f"{screenshots_dir}/GENERATOR_FOUND.png", full_page=True)
                        break

                    # Go back
                    page.goto(f"{base_url}/workspaces/12", wait_until="networkidle", timeout=60000)
                    page.wait_for_timeout(1000)
                except Exception as e:
                    print(f"      Click failed: {str(e)[:50]}")

        # Step 7: Capture page HTML structure
        print("\n[8] Capturing page structure...")
        page.goto(f"{base_url}/workspaces/12", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)

        # Get main content area
        main_html = page.evaluate("""
            () => {
                const main = document.querySelector('main, .main-content, #app, #root, body');
                return main ? main.innerHTML.substring(0, 5000) : 'No main content found';
            }
        """)

        with open(f"{screenshots_dir}/page_structure.html", "w") as f:
            f.write(main_html)
        print(f"    Saved page structure to {screenshots_dir}/page_structure.html")

        print("\n" + "=" * 60)
        print("DIAGNOSTIC COMPLETE")
        print(f"Screenshots saved to: {screenshots_dir}")
        print("=" * 60)

        browser.close()


if __name__ == "__main__":
    diagnose_rulegenai()
