from datetime import datetime, timedelta
import base64
import json


def parse_token(token: str) -> dict:
    data = token.split(".")[1]
    while len(data) % 4:
        data += '='
    
    return json.loads(base64.b64decode(data).decode())

def get_expired_time_token(token: str):
    data = parse_token(token)
    if data.get("exp") is not None:
        ts = data.get("exp")
    else:
        ts = data.get("token_expired_at")
    return datetime.utcfromtimestamp(int(ts)) - timedelta(minutes=10)