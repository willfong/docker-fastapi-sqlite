import os
import hashlib
import requests
import json
from fastapi import HTTPException
from ..services import redis, util, sqlite

def google_verify_access_token(id_token):
    # We're doing it the lazy way here. What we get from the client side is JWT, we can just verify that instead of calling Google
    # Reason for that is to reduce the amount of dependencies for this, a demo app
    # For production, we should do it the right way by using google-auth

    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}').json()
    if response.get('error'):
        errmsg = response.get('error_description')
        util.logger.error(f"[USER|google_verify_access_token] {errmsg}")
        raise HTTPException(status_code=403, detail="Invalid Google Token")
    # Here, you should check that your domain name is in hd
    # if jwt['hd'] == 'example.com':
    #   return jwt
    # For now, we're just going to accept all
    return response


FACEBOOK_URL_APP_TOKEN = f'https://graph.facebook.com/oauth/access_token?client_id={os.environ.get("FACEBOOK_CLIENT_ID")}&client_secret={os.environ.get("FACEBOOK_CLIENT_SECRET")}&grant_type=client_credentials'
def facebook_get_app_token():
    return requests.get(FACEBOOK_URL_APP_TOKEN).json()['access_token']

def facebook_verify_access_token(access_token):
    app_token = facebook_get_app_token()
    access_token_url = f'https://graph.facebook.com/debug_token?input_token={access_token}&access_token={app_token}'
    try:
        debug_token = requests.get(access_token_url).json()['data']
    except (ValueError, KeyError, TypeError) as error:
        util.logger.error(f"[USER|facebook_verify_access_token] {error}")
        return error
    user_data_url = f"https://graph.facebook.com/{debug_token['user_id']}/?&access_token={app_token}"
    user_data = requests.get(user_data_url).json()
    return user_data


def find_or_create_user(oauth_source, user_id, oauth_payload):
    user_plaintext = f"{oauth_source}|{user_id}"
    user_hash = hashlib.sha224(user_plaintext.encode('ascii')).hexdigest()
    query = "INSERT OR IGNORE INTO users (userhash, source, payload) VALUES (?,?,?)"
    params = (user_hash, oauth_source, json.dumps(oauth_payload))
    if sqlite.write(query, params):
        return user_hash
    else:
        return False


def lookup(id):
    u = redis.get(id)
    if not u:
        query = "SELECT oauth_payload FROM users WHERE userhash = ?"
        params = (id, )
        user_detail = sqlite.read(query, params, one=True)
        util.logger.warning(user_detail)
        u = {'name': 'will'}
        redis.put(id, u, 3600*24)
    return u
