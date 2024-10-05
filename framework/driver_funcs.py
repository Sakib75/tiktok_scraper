from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver import DesiredCapabilities
from time import sleep
from random import randint

def get_els(driver, xpath, time=15):
    try:
        return WebDriverWait(driver, time).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
    except:
        return []


def create_chrome_profile(profile_path):
    chrome_options = Options()
    
    # Using custom Chrome profile
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    
    # Disable unnecessary extensions and other options
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Prevent detection of automation
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Spoof user agent to mimic a real browser
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Exclude logging warnings to clean up console
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    
    # Enable performance logging for network requests
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    # Add experimental options to avoid detection
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Create and return the WebDriver instance
    return webdriver.Chrome(options=chrome_options)



def create_driver():
    chrome_profile_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "ferozprofile",
    )
    return create_chrome_profile(chrome_profile_path)

def random_scrolling(driver, scroll_total, max, min):
    current_scroll = 0
    while current_scroll < scroll_total:
        current_scroll += randint(max, min)
        driver.execute_script(f"window.scrollTo(0, {current_scroll})")
        sleep(randint(3, 6))