import logging
from selenium.webdriver import Chrome
from driver_funcs import create_driver, get_els
import sys

# Configure logging
logging.basicConfig(
    filename='login.log',  # Log output file
    filemode='a',  # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Log level
)

def login():
    driver = create_driver()
    driver.get("https://www.tiktok.com/")
    logging.info("Navigated to TikTok homepage.")

    msg = get_els(driver, "//*[@*='Open messages']")

    if msg:
        logging.info("User already logged in.")
        return True

    top_login_btn = get_els(driver, "//*[@*='top-login-button']")
    if not top_login_btn:
        logging.error("Top login button not found.")
        return False

    top_login_btn[0].click()
    logging.info("Clicked top login button.")

    email_and_phone = get_els(driver, "//*[text()='Use phone / email / username']")
    if not email_and_phone:
        logging.error("Option to use phone/email/username not found.")
        return False

    email_and_phone[0].click()
    logging.info("Clicked 'Use phone / email / username'.")

    email_and_phone2 = get_els(driver, "//*[text()='Log in with email or username']")
    if not email_and_phone2:
        logging.error("Option to log in with email or username not found.")
        return False

    email_and_phone2[0].click()
    logging.info("Clicked 'Log in with email or username'.")

    email_box = get_els(driver, "//*[@name='username']")
    if not email_box:
        logging.error("Email input box not found.")
        return False

    email_box[0].send_keys("skb09skb@gmail.com")
    logging.info("Entered username.")

    pwd_box = get_els(driver, "//*[@placeholder='Password']")
    if not pwd_box:
        logging.error("Password input box not found.")
        return False

    pwd_box[0].send_keys("Zelfh@ck11")
    logging.info("Entered password.")

    login_btn = get_els(driver, "//*[@*='login-button']")
    if not login_btn:
        logging.error("Login button not found.")
        return False

    login_btn[0].click()
    logging.info("Clicked login button.")

    msg = get_els(driver, "//*[@*='Open messages']")
    
    if msg:
        logging.info("Login Successful.")
        return True
    else:
        logging.error("Login failed.")
        return False
        sys.exit()

def search(driver, search_text):
    
if __name__ == '__main__':
    login()

    
