import json

def extract_post_info(json_data):
    if json.loads(json_data['body']).get('itemList') != None:
        posts = json.loads(json_data['body'])['itemList'] 
        all_post_data = []
        for post in posts:
            author_username = post.get('author',{}).get('uniqueId',None)
            if author_username:
                contents = post.get('contents',[])
                if contents:
                    description = contents[0]['desc']
                    unique_id = post['id']
                    video_url = f"https://www.tiktok.com/@{author_username}/video/{unique_id}"
                    all_post_data.append({
                            'author_username': author_username,
                            'video_url': video_url,
                            'description': description
                        })
        return all_post_data
    else:
        posts = json.loads(json_data['body'])['data']
        all_post_data = []
        for post in posts:
            author_username = post.get('item',{}).get('author',{}).get('uniqueId',None)
            if author_username:
                post_id = post['item']['id']
                video_url = f"https://www.tiktok.com/@{author_username}/video/{post_id}"
                description = post['item']['desc']

                all_post_data.append({
                    'author_username': author_username,
                    'video_url': video_url,
                    'description': description
                })
        
        return all_post_data
