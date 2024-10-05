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



def upload_to_database(video_data):
    con = sqlite3.connect("tiktok.db")
    cur = con.cursor()
    cur.execute("INSERT INTO post_data (search_query,author_username, video_url, description) VALUES (?, ?, ?, ?)",
                (video_data['search_query'], video_data['author_username'], video_data['video_url'], video_data['description']))
    con.commit()
    con.close()
def upload_post(posts):
    for post in posts:  
        upload_to_database(post)

import sqlite3

def fetch_all_post_data():
    conn = sqlite3.connect("tiktok.db")
    cursor = conn.cursor()
    
    try:
        # Execute a SELECT query to fetch all rows
        cursor.execute("SELECT * FROM post_data")
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        result = []
        for row in rows:
            result.append(dict(zip(column_names, row)))
        
        return result
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        pass

