#Clase MD5Hash
import hashlib

class MD5Hash():
    def md5_password(password):
        pwdBytes = password.encode(encoding='UTF-8', errors='strict')
        h = hashlib.md5()
        h.update(pwdBytes)
        return h.hexdigest()



#Clase CustomJsonEncoder
import json
from decimal import Decimal
import datetime

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        return super(CustomJsonEncoder, self).default(obj)