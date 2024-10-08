import sys
import os
import requests
from dotenv import load_dotenv
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

load_dotenv()

host = os.getenv("HOST")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

global token
global session_key

def get_token():
    res = requests.get(f'{host}/2.0/?method=auth.gettoken&api_key={api_key}&format=json')
    logging.info(f"[Auth] Get token status: {res.status_code}")
    return res.json()['token']

def get_session(token):
    signature = get_api_method_signature('auth.getSession')
    res = requests.get(f'{host}/2.0/?method=auth.getSession&token={token}&api_key={api_key}&api_sig={signature}')
    logging.info(f"[Auth] Get session status: {res.status_code}")
    return res.json()

def get_api_method_signature(method_name):
    global token
    method_sign_string = f'api_key{api_key}method{method_name}token{token}{api_secret}'
    return hashlib.md5(method_sign_string.encode()).hexdigest()

def scrobble():
    global token
    token = get_token()
    get_session(token)

def nowPlaying():
    global token
    global session_key
    
    token = get_token()
    session_key = get_session(token)
    signature = get_api_method_signature('track.updateNowPlaying')
    logging.info(f'signature: {signature}')


if __name__ == '__main__':
    # scrobble()
    nowPlaying()
    # sys.exit(0)