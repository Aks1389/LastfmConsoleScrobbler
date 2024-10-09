import sys
import os
import requests
from dotenv import load_dotenv
from hashlib import md5
import logging
import webbrowser
import json
from pathlib import Path

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

def get_session(token):
    signature = get_api_method_signature('auth.getSession')
    res = requests.get(f'{host}/2.0/?method=auth.getSession&api_key={api_key}&token={token}&api_sig={signature}&format=json')
    logging.info(f"[Auth] Get session status: {res.status_code}")
    if not res.status_code == 200:
        raise ValueError('Getting session failure.')
    return res.json()

def get_existing_session():
    return

def save_session(session , token):
    return

def authenticate():
    global token
    global session
    if(Path('./session/session1.json').exists()):
       token, session = get_existing_session()
    else:
        token = get_token()
        auth()
        session = get_session(token)
        save_session(session, token)

def get_api_method_signature(method_name):
    global token
    method_sign_string = f'api_key{api_key}method{method_name}token{token}{api_secret}'
    return md5(method_sign_string.encode('utf-8')).hexdigest()

def scrobble():
    global token
    

def nowPlaying():
    
    
    
    signature = get_api_method_signature('track.updateNowPlaying')
    res = requests.post(f"{host}/2.0/?method=track.updateNowPlaying")


if __name__ == '__main__':
    authenticate()
    # scrobble()
    nowPlaying()
    # sys.exit(0)