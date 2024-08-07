from .models import User
from jose import jwt, ExpiredSignatureError
from datetime import timezone
import datetime
from app import config

conf = config.get_settings()


def login(user_obj, expires_after=5):
    raw_data = {
        "user_id": f"{user_obj.user_id}",
        "role": "admin",
        "exp": datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=expires_after)
    }
    return jwt.encode(raw_data, conf.secret_key, conf.jwt_algo)


def verify_user_id(token):
    data = {}
    try:
        data = jwt.decode(token, conf.secret_key, conf.jwt_algo)
    except ExpiredSignatureError as e:
        print(e)
    except:
        pass
    if 'user_id' not in data:
        return None
    return data


def authenticate(email, password):
    try:
        user_obj = User.objects().get(email=email)
    except Exception as e:
        return None
    if not user_obj.verify_password(password):
        return None
    return user_obj
