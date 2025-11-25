import json
import os
from . import config
from selectolax.parser import HTMLParser

def load_raw_html(site_name):
    """
    Constructs the path based on config settings and reads the file.
    Example: raw_data/meesho_raw.html
    """
    filename = f"{site_name}_raw.html"
    filepath = os.path.join(config.RAW_DIR, filename)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[!] Error: Could not find raw file at '{filepath}'")
        print(f"    Did you run the crawler for '{site_name}' yet?")
        return None

def extract_data(html_content, parser_rules):
    """
    Extracts data using the rules defined in config.py
    """
    tree = HTMLParser(html_content)
    results = []

    # 1. Get the container selector from config
    container_selector = parser_rules['container']
    cards = tree.css(container_selector)
    
    print(f"[-] Found {len(cards)} items using selector: '{container_selector}'")

    for card in cards:
        item = {}
        
        # 2. Loop through the fields defined in config
        # fields is a dictionary: {"title": "h1", "price": "span"}
        for field_name, css_selector in parser_rules['fields'].items():
            try:
                element = card.css_first(css_selector)
                if element:
                    item[field_name] = element.text(strip=True)
                else:
                    item[field_name] = None
            except:
                item[field_name] = None
        
        # Only add valid items
        if any(item.values()):
            results.append(item)

    return results

def save_to_json(data, filename):
    """Saves data to the configured output directory."""
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[+] Successfully saved {len(data)} items to: {filepath}")

def run_parser(site_name):
    """
    Orchestrator function to run the parsing flow for a specific site.
    """
    # 1. Check if site exists in config
    if site_name not in config.SITES:
        print(f"[!] Error: Project '{site_name}' not found in config.py")
        return

    # 2. Load the specific settings
    site_config = config.SITES[site_name]
    
    # 3. Load Raw Data
    print(f"[-] Loading raw HTML for {site_name}...")
    html = load_raw_html(site_name)
    
    if html:
        # 4. Extract Data (Using the 'parser' block from config)
        print("[-] Parsing data...")
        data = extract_data(html, site_config['parser'])
        
        # 5. Save Data (Using the 'output_filename' from config)
        if data:
            save_to_json(data, site_config['output_filename'])
        else:
            print("[!] No items extracted. Check your config selectors.")

