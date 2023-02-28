from datetime import datetime
from database.manipulation import get_by, insert_into
import secrets
import jwt
import os
from utils.response import build_response
from utils.messages import USER_JUST_REGISTERED, USER_MISSING_DATA, USER_NOT_FOUND, USER_SUCCESSFULLY_REGISTERED, USER_UNSUCCESSFULLY_REGISTERED

TABLE_NAME = "users"

def save(data):
    try:
        email = data["email"]
    
        secret = secrets.token_hex()
        payload_secret = {
            "password": secret
        }
        key = f'{data["password"]}{os.environ["SECRET_KEY"]}'
        password = jwt.encode(payload_secret, key, algorithm=os.environ['DECODE_ALGORITHM'])

        created_at = str(datetime.now()).split(".")[0]
        active = True
    except:
        return build_response(message=USER_MISSING_DATA, status_code=404)
    
    try:

        if get_by("users", "email", email) is not None:
            return build_response(message=USER_JUST_REGISTERED, status_code=404)

        insert_into(TABLE_NAME, ("email", "password", "secret_key", "created_at", "active"), \
        (email, password, secret, created_at, active))
    except Exception as e:
        return build_response(message=USER_UNSUCCESSFULLY_REGISTERED, status_code=500)

    return build_response(message=USER_SUCCESSFULLY_REGISTERED, status_code=200)


def get(email):
    result = get_by(TABLE_NAME, "email", email)
    
    if result is None:
        return build_response(message=USER_NOT_FOUND, status_code=404)
 
    response = {
        "user_id": result[0],
        "email": result[1],
        "created_at": str(result[5]),
        "is_active": result[6]
    }

    return build_response(message=email, data=response, status_code=200)