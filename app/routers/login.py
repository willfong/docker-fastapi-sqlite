import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services import user, util, statsd

router = APIRouter()

class LoginToken(BaseModel):
    value: str

def create_login_token(sub):
    token = jwt.encode({
        'sub': sub,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        util.get_secret_token())
    return token


@router.post("/facebook")
@statsd.statsd_root_stats
def login_facebook(token: LoginToken):
    facebook_data = user.facebook_verify_access_token(token.value)
    user_id = user.find_or_create_user('facebook', facebook_data['id'], facebook_data)
    return {"token": create_login_token(user_id)}


@router.post("/google")
@statsd.statsd_root_stats
def login_google(token: LoginToken):
    google_data = user.google_verify_access_token(token.value)
    user_id = user.find_or_create_user('google', google_data['sub'], google_data)
    return {"token": create_login_token(user_id)}


@router.post("/test-account")
@statsd.statsd_root_stats
def login_test(username: LoginToken):
    user_id = user.find_or_create_user('test-account', username.value, {"name": username.value})
    util.logger.warning(f"Test Account Logged In: {user_id}")
    if user_id:
        return {"token": create_login_token(user_id)}
    else:
        return {"error": "could not log in"}

@router.get("/lookup")
@statsd.statsd_root_stats
def lookup(id: str):
    return user.lookup(id)