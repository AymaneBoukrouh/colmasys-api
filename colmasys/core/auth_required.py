from colmasys import auth as colmasys_auth
from colmasys.models import User
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

### utils
def check_authorization_level(auth, user_type):
    payload = colmasys_auth.decode_token(auth.credentials)
    if payload.get('type') == user_type:
        return payload.get('uid')
    else:
        raise HTTPException(status_code=401, detail='Permission Denied')

### authorization required
def auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return colmasys_auth.decode_token(auth.credentials).get('uid')

def admin_auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return check_authorization_level(auth, User.Type.admin)

def professor_auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return check_authorization_level(auth, User.Type.professor)

def student_auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return check_authorization_level(auth, User.Type.student)
