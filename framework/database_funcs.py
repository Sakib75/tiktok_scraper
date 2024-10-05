import sqlite3

import sqlite3

def create_database_and_table():
    # Connect to the database (this will create it if it doesn't exist)
    conn = sqlite3.connect("tiktok.db")
    cursor = conn.cursor()

    # Create the post_data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS post_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_query TEXT,
        author_username TEXT,
        video_url TEXT,
        description TEXT
    )
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database and table created successfully.")



def upload_to_database(video_data):
    con = sqlite3.connect("tiktok.db")
    cur = con.cursor()
    cur.execute("INSERT INTO post_data (search_query,author_username, video_url, description) VALUES (?, ?, ?, ?)",
                (video_data['search_query'], video_data['author_username'], video_data['video_url'], video_data['description']))
    con.commit()
    con.close()
    print('Uploaded')

def upload_post(posts):
    for post in posts:  
        upload_to_database(post)

sample_data = [{
    "search_query":"a",
    "author_username":"b",
    "video_url":"c",
    "description":"d"
},
{
    "search_query":"a",
    "author_username":"b",
    "video_url":"c",
    "description":"d"
},
]

create_database_and_table()
upload_post(sample_data)

