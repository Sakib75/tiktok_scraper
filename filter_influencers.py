import pandas as pd

df = pd.read_csv('username_info.csv')
filtered_df = df[df['follower'] > 100000 and df['like_count'] > 10000000]

filtered_df.to_csv('filtered_username_info.csv', index=False)