import os
import jwt
from utils.messages import INVALID_TOKEN, LOGIN_NOT_CORRESPOND_WITH_DEVICE, LOGIN_SUCCESSFUL, SUCCESSFULLY_AUTHENTICATED, USER_NOT_FOUND, WRONG_PASSWORD
from utils.response import build_response

from database.manipulation import get_by, update_by

def login(data, ip):
    email = data["email"]

    user = get_by("users", "email", email)

    if user is not None:
        encrypted_pass = user[2]
        secret = user[4]

        try:
            key = f"{data['password']}{os.environ['SECRET_KEY']}"
            obj = jwt.decode(encrypted_pass, key, algorithms=[os.environ['DECODE_ALGORITHM']])

            if obj["password"] == secret:
                encrypted_ip = jwt.encode({"ip": ip}, os.environ["SECRET_KEY"], algorithm=os.environ['DECODE_ALGORITHM'])

                update_by("users", "email", email, "last_access_ip", encrypted_ip)

                payload = {
                    "email": email,
                    "secret": secret,
                    "ip": encrypted_ip
                }

                auth_token = jwt.encode(payload, os.environ["SECRET_KEY"], algorithm=os.environ['DECODE_ALGORITHM'])

                return build_response(message=LOGIN_SUCCESSFUL, status_code=200, data={"auth_token": auth_token})
        except:
            return build_response(message=WRONG_PASSWORD, status_code=400)

    return build_response(message=USER_NOT_FOUND, status_code=404)

def check_token(token:str, ip):
    obj = None

    try:
        token = token.split()[1]
        obj = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=[os.environ['DECODE_ALGORITHM']])
    except Exception as e:
        return False, INVALID_TOKEN, None

    email = obj['email']

    if get_by("users", "email", email) is None:
        return False, INVALID_TOKEN, None

    ip_obj = obj["ip"]
    ip_obj = jwt.decode(ip_obj, os.environ['SECRET_KEY'], algorithms=[os.environ['DECODE_ALGORITHM']])

    if ip_obj['ip'] != ip:
        return False, LOGIN_NOT_CORRESPOND_WITH_DEVICE, None
    
    return True, SUCCESSFULLY_AUTHENTICATED, obj


def get_account(token:str, ip):
    valid, message, obj = check_token(token, ip)
    return build_response(message, status_code=400 if not valid else 200, data=obj if not valid else {'email' : obj['email']}) 
