import logging
from selenium.webdriver import Chrome
from framework.driver_funcs import create_driver, get_els, random_scrolling
import sys
import json
from framework.extract_info import extract_post_info
from framework.database_funcs import upload_post
from time import sleep
from random import randint

def process_browser_log_entry(entry):
    response = json.loads(entry["message"])["message"]
    return response

# Configure logging
logging.basicConfig(
    filename='tiktok_scraper.log',  # Log output file
    filemode='a',  # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Log level
)

logger = logging.getLogger('tiktok_scraper')

def login(driver: Chrome):
    try:
        driver.get("https://www.tiktok.com/")
        logger.info("Navigated to TikTok homepage.")

        msg = get_els(driver, "//*[@*='Open messages']")
        if msg:
            logger.info("User already logged in.")
            return True

        top_login_btn = get_els(driver, "//*[@*='top-login-button']")
        if not top_login_btn:
            logger.error("Top login button not found.")
            return False

        top_login_btn[0].click()
        logger.info("Clicked top login button.")

        email_and_phone = get_els(driver, "//*[text()='Use phone / email / username']")
        if not email_and_phone:
            logger.error("Option to use phone/email/username not found.")
            return False

        email_and_phone[0].click()
        logger.info("Clicked 'Use phone / email / username'.")

        email_and_phone2 = get_els(driver, "//*[text()='Log in with email or username']")
        if not email_and_phone2:
            logger.error("Option to log in with email or username not found.")
            return False

        email_and_phone2[0].click()
        logger.info("Clicked 'Log in with email or username'.")

        email_box = get_els(driver, "//*[@name='username']")
        if not email_box:
            logger.error("Email input box not found.")
            return False

        email_box[0].send_keys("skb09skb@gmail.com")
        logger.info("Entered username.")

        pwd_box = get_els(driver, "//*[@placeholder='Password']")
        if not pwd_box:
            logger.error("Password input box not found.")
            return False

        pwd_box[0].send_keys("Zelfh@ck11")
        logger.info("Entered password.")

        login_btn = get_els(driver, "//*[@*='login-button']")
        if not login_btn:
            logger.error("Login button not found.")
            return False

        login_btn[0].click()
        logger.info("Clicked login button.")

        msg = get_els(driver, "//*[@*='Open messages']")
        
        if msg:
            logger.info("Login Successful.")
            return True
        else:
            logger.error("Login failed.")
            return False

    except Exception as e:
        logger.exception(f"An error occurred during login: {e}")
        sys.exit()

def search(driver: Chrome, search_text: str, scroll_total: int):
    try:
        logger.info(f"Starting search for query: {search_text}")
        
        if search_text.startswith("#"):
            # Do some random scrolling 
            random_scrolling(driver, 400, 100,200)
            driver.get(f"https://www.tiktok.com/tag/{search_text[1:]}")
            logger.info(f"Navigated to hashtag page: {search_text}")
        else:
            search_box = get_els(driver, "//input[@*='Search']")
            if not search_box:
                logger.error("Search box not found.")
                return False
            search_box[0].send_keys(search_text)

            search_btn = get_els(driver, "//*[@*='search-box-button']")
            if not search_btn:
                logger.error("Search button not found.")
                return False
            search_btn[0].click()
            logger.info(f"Clicked search button for query: {search_text}")

        current_scroll = 0
        while current_scroll < scroll_total:
            current_scroll += randint(500, 800)
            driver.execute_script(f"window.scrollTo(0, {current_scroll})")
            sleep(randint(3, 6))
            logger.info(f"Scrolled to position {current_scroll}")

        browser_log = driver.get_log("performance")
        events = [process_browser_log_entry(entry) for entry in browser_log]

        if search_text.startswith("#"):
            api_responses = []
            for event in events:
                if "response" in event["params"]:
                    if (
                        "https://www.tiktok.com/api/challenge/item_list/?WebIdLastTime" 
                        in event.get("params", {}).get("response", {}).get("url", "")
                    ):
                        request_id = event["params"]["requestId"]
                        logger.info(f"Captured request ID: {request_id}")
                        try:
                            api_response = driver.execute_cdp_cmd(
                                "Network.getResponseBody",
                                {"requestId": str(request_id)},
                            )
                            api_responses.append(api_response)
                        except:
                            logger.info("No response found")

            all_post_data = []
            for api_response in api_responses:
                post_data = extract_post_info(api_response)
                all_post_data.append(post_data)
            
        if not search_text.startswith("#"):
            api_responses = []
            for event in events:
                if "response" in event["params"]:
                    if (
                        "https://www.tiktok.com/api/search/general/full/?WebIdLastTime" 
                        in event.get("params", {}).get("response", {}).get("url", "")
                    ):
                        request_id = event["params"]["requestId"]
                        logger.info(f"Captured request ID: {request_id}")
                        try:
                            api_response = driver.execute_cdp_cmd(
                                "Network.getResponseBody",
                                {"requestId": str(request_id)},
                            )
                            api_responses.append(api_response)
                        except:
                            logger.info("No response found")

        all_post_data = []
        for api_response in api_responses:
            post_data = extract_post_info(api_response)
            all_post_data.append(post_data)

        all_data_to_upload = []
        for all_post in all_post_data:
            for post in all_post:
                post['search_query'] = search_text
                all_data_to_upload.append(post)
            
        upload_post(all_data_to_upload)
        logger.info(f"Uploaded {len(all_data_to_upload)} posts to the database for query: {search_text}")

    except Exception as e:
        logger.exception(f"An error occurred during search: {e}")

if __name__ == '__main__':
    try:
        driver = create_driver()
        logger.info("Driver created successfully.")
        
        if login(driver):
            logger.info("Login successful, starting search.")
            search(driver, "places to visit", 500)
        else:
            logger.error("Login failed. Exiting.")

    except Exception as e:
        logger.exception(f"An error occurred in the main process: {e}")

    finally:
        if driver:
            driver.quit()
            logger.info("Driver closed successfully.")
