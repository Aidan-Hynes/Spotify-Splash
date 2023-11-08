import base64
import json
from urllib.parse import urlencode
from requests import get, post


CLIENT_ID = // CLIENT_ID
CLIENT_SECRET = // CLIENT_SECRET


def get_user_auth():
    url = 'https://accounts.spotify.com/authorize?'

    query = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": // redirect_uri,
        "scope": "user-read-playback-state user-read-currently-playing"
    }
    coded_query = urlencode(query)

    return url + coded_query


def get_first_token(auth_code):
    auth_string = CLIENT_ID + ':' + CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": // redirect_uri
    }

    result = post(url, headers=headers, data=data)
    print(result.content)
    json_result = json.loads(result.content)
    access_token = json_result['access_token']
    refresh_token = json_result['refresh_token']

    return access_token, refresh_token


def get_new_token(refresh_token):
    auth_string = CLIENT_ID + ':' + CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    result = post(url, headers=headers, data=data)
    print(result.content)
    json_result = json.loads(result.content)
    access_token = json_result['access_token']

    return access_token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_album_cover(token):
    url = 'https://api.spotify.com/v1/me/player/currently-playing?country=CAN'
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    try:
        if json.loads(result.content)['is_playing']:
            return json.loads(result.content)['item']['album']['images'][0]
        print('No song playing')
    except:
        print('No active device')
    return None
