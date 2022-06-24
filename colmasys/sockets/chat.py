from colmasys import app
from colmasys.core import auth_required
from fastapi import Depends

@app.sio.on('okokok')
async def handle_connect(sid, authenticated_user_id=Depends(auth_required.auth_required), **kwargs):
    print(kwargs)
    print(f'New device connected')