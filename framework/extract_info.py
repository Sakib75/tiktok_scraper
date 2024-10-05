import json

def extract_post_info(json_data):
    posts = json.loads(json_data['body'])['data']
    all_post_data = []
    for post in posts:
        author_username = post['item']['author']['uniqueId']
        post_id = post['item']['id']
        video_url = f"https://www.tiktok.com/@{author_username}/video/{post_id}"
        description = post['item']['desc']

        all_post_data.append({
            'author_username': author_username,
            'video_url': video_url,
            'description': description
        })
    
    return all_post_data
