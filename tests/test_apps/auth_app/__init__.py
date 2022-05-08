from colmasys.core import auth_required
from fastapi import FastAPI, Depends

testapp = FastAPI()

### endpoints
@testapp.get('/unprotected')
async def unprotected():
    return {'status': 'success'}

@testapp.get('/protected')
async def protected(user_id=Depends(auth_required.auth_required)):
    return {'status': 'success'}

@testapp.get('/any_user')
async def any_user(user_id=Depends(auth_required.auth_required)):
    return {'status': 'success'}

@testapp.get('/admin_only')
async def admin_only(user_id=Depends(auth_required.admin_auth_required)):
    return {'status': 'success'}

@testapp.get('/professor_only')
async def professor_only(user_id=Depends(auth_required.professor_auth_required)):
    return {'status': 'success'}

@testapp.get('/student_only')
async def professor_only(user_id=Depends(auth_required.student_auth_required)):
    return {'status': 'success'}
