from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

### environment variables
load_dotenv()
SECRET = os.environ['SECRET']

### models
class AuthCreds(BaseModel):
    username: str
    password: str

    @property
    def data(self) -> tuple:
        return self.username, self.password

### handlers
class Auth():
    security = HTTPBearer()
    secret = SECRET

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def encode_token(self, user_id: int, user_type) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'uid': user_id,
            'type': user_type
        }

        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token: str) -> int:
        try:
            return jwt.decode(token, self.secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature Expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail = 'Invalid Token')
