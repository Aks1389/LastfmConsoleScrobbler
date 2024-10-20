import sys
import os
import requests
from dotenv import load_dotenv
from hashlib import md5
import logging
import webbrowser
import json
from pathlib import Path
import id3_tags_reader

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

load_dotenv()

host = os.getenv("HOST")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

global token
global session

def get_token():
    res = requests.get(f'{host}/2.0/?method=auth.gettoken&api_key={api_key}&format=json')
    logging.info(f"[Auth] Get token status: {res.status_code}")
    if not res.status_code == 200:
        raise ValueError('Getting token failure.')
    return res.json()['token']

def auth():
    webbrowser.open(f"http://www.last.fm/api/auth/?api_key={api_key}&token={token}", new=0, autoraise=True)
    input('Press Enter to continue...')

def get_session(token):
    sign_params = {'method': 'auth.getSession', 'api_key': api_key, 'token': token}
    signature = get_api_method_signature(sign_params)
    res = requests.get(f'{host}/2.0/?method=auth.getSession&api_key={api_key}&token={token}&api_sig={signature}&format=json')
    logging.info(f"[Auth] Get session status: {res.status_code}")
    if not res.status_code == 200:
        raise ValueError('Getting session failure.')
    return res.json()

def get_existing_session(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data['session']['key'], data['session']['token']

def save_session(path, session , token):
    session['session']['token'] = token
    json_object = json.dumps(session, indent=4)
 
    with open(path, "x") as outfile:
        outfile.write(json_object)

def authenticate():
    global token
    global session
    path = './session/session1.json'
    if(Path(path).exists()):
        logging.info("[Auth] An existing session found.")
        session, token = get_existing_session(path)
    else:
        logging.info("[Auth] There is no session found. Will be created a new one.")
        token = get_token()
        auth()
        session = get_session(token)
        save_session(path, session, token)

def get_api_method_signature(params_dict):
    global token
    keys = sorted(params_dict.keys())
    method_sign_string = [k + str(params_dict[k]) for k in keys]
    method_sign_string = "".join(method_sign_string) + api_secret
    return md5(method_sign_string.encode('utf-8')).hexdigest()

def scrobble(track_list):
    body = {
        "method": "track.scrobble",
        "api_key": api_key,
        "sk": session
        }
    body.update(track_list)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    signature = get_api_method_signature(body)
    body['api_sig'] = signature
    res = requests.post(url=f"{host}/2.0/", data=body, headers=headers)
    if not res.status_code == 200:
        print(res.text)
        raise ValueError('Scrobbling didn\'t worked.')
    logging.info("Scrobbling:" + res.text)
    
def nowPlaying():
    """api: https://www.last.fm/api/show/track.updateNowPlaying"""
    body = {
        "method": 'track.updateNowPlaying',
        "artist": 'Dark Tranquillity',
        "track": 'Damage Done',
        "album": 'Damage Done',
        "api_key": api_key,
        "sk": session
        }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    signature = get_api_method_signature(body)
    body['api_sig'] = signature
    res = requests.post(url=f"{host}/2.0/", data=body, headers=headers)
    if not res.status_code == 200:
        print(res.text)
        raise ValueError('Now playing didn\'t worked.')
    logging.info("NowPlaying:" + res.text)


if __name__ == '__main__':
    authenticate()
    filepath = input("Enter track-list file path: ")
    start_time = input("Enter start time(dd-mm-yyyy_hh:mm +0300): ")
    # filepath = "C:\\Users\\aksnv\\Documents\\Programming\\Last.fm Scrobbler\\tracklist.txt"
    # start_time = "15-10-2024_19:00 +0300"
    tracklist = id3_tags_reader.get_track_list(filepath, start_time)
    
    scrobble(tracklist)
    # nowPlaying()
    # sys.exit(0)