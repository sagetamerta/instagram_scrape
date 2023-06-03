import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from tzlocal import get_localzone

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Get the local time zone
timezone = get_localzone()
# Get the current time in the local time zone
current_time = datetime.now(timezone)

# Load variables from .env file
load_dotenv()

# get env
COOKIE = os.getenv("COOKIE")
CSRF_TOKEN = os.getenv("CSRF_TOKEN")
APP_ID = os.getenv("APP_ID")
WWW_CLAIM = os.getenv("WWW_CLAIM")

# get user input for instagram username
username = input('Enter the username: ')

# init request url api instagram for get user info
requestUrl = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

# init header
headerRequest = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
    'Cache-Control': 'no-cache',
    'Cookie': COOKIE,
    'Dnt': '1',
    'Pragma': 'no-cache',
    'Referer': f'https://www.instagram.com/{username}/',
    'X-Csrftoken': CSRF_TOKEN,
    'X-Ig-App-Id': APP_ID,
    'X-Ig-Www-Claim': WWW_CLAIM,
    'X-Requested-With': 'XMLHttpRequest'
}

response = requests.get(url=requestUrl, headers=headerRequest)

if response.status_code == 200:

    # get user response
    json_response = response.json()
    # convert json dict to string
    json_string = json.dumps(json_response)
    # delete all space in the string
    json_string_response_without_spaces = json_string.replace(" ", "")

    # set folder name
    folder_name = 'export'

    # set filename for export into json file
    file_name = f"{username}_response.json"
    export_path = os.path.join(folder_name, file_name)

    # Create the "exports" folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    # after converted to string, convert back to dict type
    json_converted_dict = json.loads(json_string_response_without_spaces)

    userdata = json_converted_dict["data"]["user"]
    followers_count = userdata["edge_followed_by"]["count"]
    following_count = userdata["edge_follow"]["count"]

    print(f'followers count: ', followers_count)
    print(f'following count: ', following_count)

    data_for_export = {
        'username': username,
        'followers': followers_count,
        'following': following_count,
        'current_time': current_time
    }

    export_data = json.dumps(data_for_export, cls=DateTimeEncoder)
    converted_export_data = json.loads(export_data)

    if os.path.isfile(export_path) and os.path.getsize(export_path) > 0:
        with open(export_path, 'r+') as file:
            file_data = json.load(file)
            file_data.append(converted_export_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    else:
        with open(export_path, 'w') as file:
            json.dump([converted_export_data], file, indent=4)

    print(f'JSON response saved to {export_path}.')

else:
    print('Request failed with status code:', response.status_code)
