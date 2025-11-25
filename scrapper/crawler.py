import os
import time
from . import config
from playwright.sync_api import sync_playwright
# We use the clean import now because you have the new version
from playwright_stealth import Stealth

def perform_physical_login(page, auth_config):
    """Handles manual login if cookies fail."""
    print("[-] Cookies missing or expired. Logging in physically...")
    
    page.goto(auth_config['login_url'])
    page.fill(auth_config['username_selector'], auth_config['credentials']['user'])
    page.fill(auth_config['password_selector'], auth_config['credentials']['pass'])
    page.click(auth_config['submit_selector'])
    
    try:
        page.wait_for_selector(auth_config['success_selector'], timeout=15000)
        print("[+] Login Successful!")
        return True
    except:
        print("[!] Login Failed (Captcha or Wrong Password).")
        return False

def crawl(site_name):
    # 1. Load Rules from Config
    site_config = config.SITES[site_name]
    rules = site_config.get('crawling_rules', {'max_scrolls': 5, 'scroll_delay': 2})

    print(f"[-] Starting crawler for: {site_name.upper()}")

    with sync_playwright() as p:
        # 2. Launch Browser (Using Central Settings)
        browser = p.chromium.launch(**config.BROWSER_ARGS)
        
        # 3. Session Handling (Load Cookies if they exist)
        context_options = config.CONTEXT_ARGS.copy()
        auth_file = None
        
        if site_config['requires_login']:
            auth_file = site_config['auth']['cookie_file']
            if os.path.exists(auth_file):
                print(f"[-] Loading session from {auth_file}")
                context_options['storage_state'] = auth_file
        
        context = browser.new_context(**context_options)
        page = context.new_page()
        
        # 4. APPLY STEALTH (The Clean Way)
        Stealth().apply_stealth_sync(page)

        # 5. Navigation & Auto-Login
        try:
            if site_config['requires_login']:
                page.goto(site_config['url'], timeout=60000)
                try:
                    page.wait_for_load_state("networkidle", timeout=5000)
                except: pass

                # Check if we got kicked out
                if page.is_visible(site_config['auth']['username_selector']):
                    print("[!] Session expired. Re-logging...")
                    if perform_physical_login(page, site_config['auth']):
                        # Save fresh cookies
                        context.storage_state(path=auth_file)
                        page.goto(site_config['url'])
                    else:
                        browser.close()
                        return None
            else:
                print(f"[-] Navigating to {site_config['url']}")
                page.goto(site_config['url'], timeout=60000)
        
        except Exception as e:
            print(f"[!] Navigation error: {e}")
            browser.close()
            return None

        # 6. Scroll Loop (Time/Quantity Logic)
        print("[-] Starting Scroll Phase...")
        for i in range(1, rules['max_scrolls'] + 1):
            page.mouse.wheel(0, rules.get('scroll_distance', 3000))
            time.sleep(rules['scroll_delay'])
            print(f"    [Scroll {i}/{rules['max_scrolls']}] Loading data...")
            
        print("[-] Scrolling complete.")
        
        # 7. Extract & Save
        html = page.content()
        browser.close()
        
        filename = f"{site_name}_raw.html"
        filepath = os.path.join(config.RAW_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[+] Saved raw HTML to {filepath}")
        
        return html