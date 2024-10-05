from framework.driver_funcs import create_driver, get_els
from framework.database_funcs import fetch_all_post_data
from time import sleep
from random import randint

driver = create_driver()


all_data = fetch_all_post_data()
print(all_data)

import pandas as pd

df = pd.DataFrame(all_data)

unique_usernames = df['author_username'].unique()

all_username_info = []
for username in unique_usernames:
    print(f"Username: {username}")
    driver.get(f"https://www.tiktok.com/@{username}")

    following = get_els(driver,"//strong[@title='Following']")
    following = following[0].text

    follower = get_els(driver,"//strong[@title='Followers']")
    follower = follower[0].text

    likes = get_els(driver, "//strong[@title='Likes']")
    likes = likes[0].text
    all_username_info.append({
        "username": username,
        "following": following,
        "follower": follower,
        "likes": likes
    })

    sleep(randint(3,6))

pd.DataFrame(all_username_info).to_csv("username_info.csv", index=False)
    
