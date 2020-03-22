import os
import hashlib
import requests
from fastapi import HTTPException
from ..services import ddb, redis, util, statsd

@statsd.statsd_root_stats
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
@statsd.statsd_root_stats
def facebook_get_app_token():
    return requests.get(FACEBOOK_URL_APP_TOKEN).json()['access_token']

@statsd.statsd_root_stats
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


@statsd.statsd_root_stats
def find_or_create_user(oauth_source, user_id, oauth_payload):
    user_plaintext = f"{oauth_source}|{user_id}"
    user_hash = hashlib.sha224(user_plaintext.encode('ascii')).hexdigest()
    key = {'id': user_hash}
    expression = "SET #source = :source, #payload = :payload"
    names = {'#source': 'oauth_source', '#payload': 'oauth_payload'}
    values = {':source': oauth_source, ':payload': oauth_payload}
    if ddb.upsert(ddb.USERS, key, expression, names, values):
        return user_hash
    else:
        raise HTTPException(status_code=500, detail="Could not create user. Try again later.")


@statsd.statsd_root_stats
def lookup(id):
    u = redis.get(id)
    if not u:
        d = ddb.get(ddb.USERS, {'id': id})
        u = {'name': d['oauth_payload'].get('name')}
        redis.put(id, u, 3600*24)
    return u
