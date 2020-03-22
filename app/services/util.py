import os
import jwt
import requests
import logging


logger = logging.getLogger(__name__)
myFormatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(myFormatter)
logger.addHandler(handler)


def get_user_data_from_token(token):
    token_dict = verify_token(token)
    if token_dict:
        return token_dict
    logger.error(f'Could not verify token: {token}')
    return False

def get_secret_token():
    # TODO: Obviously, this should be updated to AWS KMS
    return 'SECRET_TOKEN_HERE'

def verify_token(token):  
    try: 
        response = jwt.decode(token, get_secret_token())
    except:
        logger.error(f'Bad token: {token}')
        return False
    return response
