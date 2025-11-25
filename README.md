# Python Web Scraper

A configurable, multiprocessing web scraper built with **Playwright** (for browsing) and **Selectolax** (for parsing). 

This project demonstrates a **staged pipeline architecture**, separating the "fetching" logic from the "extraction" logic to make the system more robust against website changes.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-Browser_Automation-orange?logo=playwright)

---

## 💡 The Idea

Most tutorials put scraping and parsing in one big loop. If the parsing fails, you lose the data. 
I designed this project to solve that by decoupling the process:

1.  **Crawler:** Opens the browser, handles login/scrolling, and saves **Raw HTML**.
2.  **Parser:** Reads the Raw HTML from disk and extracts JSON data using CSS selectors.

This means if my selectors break, I don't have to re-scrape the website. I just fix the selectors and re-run the parser on the saved HTML.

---

## 🛠️ Tech Stack

*   **Playwright (Sync):** Used for browser automation. It handles dynamic content (JavaScript), login flows, and infinite scrolling better than `requests`.
*   **Selectolax:** Used for parsing HTML. It is significantly faster and more lightweight than `BeautifulSoup`.
*   **ProcessPoolExecutor:** Used to run multiple browser instances simultaneously (Multiprocessing) to speed up the workflow.
*   **Playwright-Stealth:** Patches the browser fingerprint to look more human.

---

## ✨ Key Features

The code is organized to separate concerns:

Config-Driven: You don't need to touch the code to scrape a new site. You just add a dictionary entry to config.py.

Self-Healing Login: The crawler checks if the session is valid. If cookies are expired, it performs a physical login and updates the cookie file automatically.

Raw Data Storage: Saves the page state immediately, ensuring no data loss if the extraction logic fails.

Human Emulation: Uses slow_mo and random scroll delays to mimic human behavior.

## 🚀 How to Run
### Make Vertual Enviroments(recommended)

`python -m venv .venv`

**for linux and MacOS**
<br>
`source .venv/bin/activate`

**for window terminal**
<br>
`venv\Scripts\activate`

### Install Dependencies

**`pip install -r requirements.txt`**

`playwright install chromium`

### Setup Credentials(if needed)

Create a .env file in the root folder:

`USER=your_email/username
`
`PASSWORD=your_password
`
### Run the Pipeline

**`python main.py`**

This will trigger the multiprocessing pool, launch the browsers, and save the results to the output_data folder.

## ⚙️ Configuration Example (config.py)

***Visit config.py for understand and change configaration.***


## 📝 Disclaimer

This project is for educational purposes. Web scraping should be done responsibly. Please respect robots.txt and the Terms of Service of the target websites.

