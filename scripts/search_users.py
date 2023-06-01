import requests
import json
import os
from dotenv import load_dotenv

username = input('Enter the username: ')

url = 'https://www.instagram.com/api/v1/web/search/topsearch/'

COOKIE = os.getenv("COOKIE")
CSRF_TOKEN = os.getenv("CSRF_TOKEN")
APP_ID = os.getenv("APP_ID")
WWW_CLAIM = os.getenv("WWW_CLAIM")

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': COOKIE,
    'Referer': f'https://www.instagram.com/{username}/',
    'X-Csrftoken': CSRF_TOKEN,
    'X-Ig-App-Id': APP_ID,
    'X-Ig-Www-Claim': WWW_CLAIM,
    'X-Requested-With': 'XMLHttpRequest',
}

params = {
    'context': 'blended',
    'query': f'{username}',
    'rank_token': '0.1',
    'include_reel': 'false',
    'search_surface': 'web_top_search'
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:

    json_response = response.json()
    json_string = json.dumps(json_response)
    json_string_response_without_spaces = json_string.replace(" ", "")
    json_converted_dict = json.loads(json_string_response_without_spaces)

    userdata = json_converted_dict["users"]
    
    for item in userdata:
        user = item["user"]
        print("Username:", user["username"])
        print("Full Name:", user["full_name"])
        print("Profile pic url:", user["profile_pic_url"])
        print("-----------------------------------")

else:
    print('Request failed with status code:', response.status_code)
