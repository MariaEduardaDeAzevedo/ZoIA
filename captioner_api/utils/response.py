from flask import Response
import json

def build_response(message, status_code, data=None):
    response_body = {
        "message": message,
        "data": data,
        "status_code": status_code
    }

    response = Response(response=json.dumps(response_body), status=status_code)

    return response