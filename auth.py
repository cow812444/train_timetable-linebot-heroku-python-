from hashlib import sha1
import hmac
import base64
from wsgiref.handlers import format_date_time
from time import mktime
from datetime import datetime
import os

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# 透過app_id & app_key計算hmac-sha1 key
class Auth(metaclass=Singleton):
    def __init__(self):
        # 台鐵 Access App_id token
        self.app_id = os.environ.get('APP_ID')
        # 台鐵 Access App_key token
        self.app_key = os.environ.get('APP_KEY')

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }
