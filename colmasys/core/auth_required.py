from colmasys import auth as colmasys_auth
from colmasys.models import Account
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

### utils
def check_authorization_level(auth: HTTPAuthorizationCredentials, account_type: Account.Type):
    payload = colmasys_auth.decode_token(auth.credentials)
    if payload.get('account_type') == account_type:
        return payload.get('account_id')
    else:
        raise HTTPException(status_code=401, detail='Permission Denied')

### authorization required
def auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return colmasys_auth.decode_token(auth.credentials).get('account_id')

def admin_auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return check_authorization_level(auth, Account.Type.Admin)

def professor_auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return check_authorization_level(auth, Account.Type.Professor)

def student_auth_required(auth:HTTPAuthorizationCredentials=Security(colmasys_auth.security)):
    return check_authorization_level(auth, Account.Type.Student)
