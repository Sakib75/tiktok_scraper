import pandas as pd
from framework.tiktok_bot import login, search
from framework.driver_funcs import create_driver
from time import sleep
from random import randint
from framework.logging_config import logger





if __name__ == "__main__":
    scroll_total = 3000
    logger.info("Starting TikTok scraping script")
    
    try:
        driver = create_driver()
        logger.info("Web driver created successfully")
        
        login(driver)
        logger.info("Logged in to TikTok")
        
        input_df = pd.read_csv('queries.csv')
        logger.info(f"Loaded {len(input_df)} queries from queries.csv")
        
        for i in range(10, len(input_df)):
            search_query = input_df.loc[i, 'Query']
            logger.info(f"Searching for query: {search_query}")
            
            search(driver, search_query, scroll_total)
            logger.info(f"Completed search for: {search_query}")
            
            sleep_time = randint(20, 30)
            logger.info(f"Sleeping for {sleep_time} seconds before next query")
            sleep(sleep_time)
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    finally:
        if driver:
            driver.quit()
            logger.info("Driver closed successfully")
