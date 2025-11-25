import os
from dotenv import load_dotenv

load_dotenv()

# 1. FILE SYSTEM SETTINGS
# Where to save the raw HTML files
RAW_DIR = "raw_data"
# Where to save the final JSON files
OUTPUT_DIR = "output_data"

# Create directories if they don't exist
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# 2. BROWSER SETTINGS (The "Engine" Rules)
BROWSER_ARGS = {
    "headless": True,       # Set True to run invisibly
    "slow_mo": 100,         # Wait 100 ms between actions (Human mode)
    "args": [
        "--disable-blink-features=AutomationControlled", # Hide "Robot" flag
    ]
}

CONTEXT_ARGS = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "viewport": {"width": 1366, "height": 768},
    "locale": "en-US",
    "timezone_id": "Asia/Kolkata"
}


# 3. SITE CONFIGURATIONS (The "Map")
# You can switch projects just by changing one variable in your main script.

SITES = {
    #  PROJECT 1:  (No Login, Public Data) 
    "comapny": {
        "url": "https://www.meesho.com/women-ethnic-wear/clp/1hjl",
        "requires_login": False,
        "output_filename": "company_products.json",
        
        # PARSER RULES (Used by parser.py)
        "parser": {
            "container": "div[class*='ProductCard']",
            "fields": {
                "title": "p[class*='ProductTitle']",
                "price": "h5",
                "discount": "span[class*='Discount']",
                "rating": "span[class*='Rating']",
                "delivery": "span[class*='EstimatedDelivery']"
            }
        },
        
    },

    #  PROJECT 2:  (Login Required)
    "example": {
        "url": "https://www.example.com/feed/",
        "requires_login": True,
        
        # LOGIN RULES (Used by crawler.py)
        "auth": {
            "login_url": "https://www.example.com/login",
            "cookie_file": "example_cookies.json",
            "username_selector": "#username",
            "password_selector": "#password",
            "submit_selector": "button[type='submit']",
            "success_selector": ".global-nav__me-photo", # Proof we are logged in
            "credentials": {
                "user": os.getenv("USER"), # Reads from .env
                "pass": os.getenv("PASSWORD")  # Reads from .env
            }
        },
        
        # PARSER RULES
        "parser": {
            "container": "div.feed-shared-update-v2", # Example: A post
            "fields": {
                "author": "span.update-components-actor__name",
                "text": "span.break-words"
            }
        }
    }
}
