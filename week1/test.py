import uuid
import os
from datetime import datetime
import jwt

payload = {
    'exp': datetime.utcnow(),
    'iat': datetime.utcnow(),
    'sub': id
}

token =  jwt.encode(
    payload,
    'top-secret',
    algorithm='HS256'
)
       
print(token.decode())