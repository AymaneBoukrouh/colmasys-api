from colmasys.models import User, UserModel
from sqlalchemy import select
import uuid

async def user_filter_by_scalars(session, **kwargs):
    query = select(User).filter_by(**kwargs)
    result = await session.execute(query)
    return result.scalars()

async def get_user_by(session, **kwargs):
    scalars = await user_filter_by_scalars(session, **kwargs)
    return scalars.first()

async def get_users_by_type(session, user_type: User.Type):
    scalars = await user_filter_by_scalars(session, user_type=user_type)
    users = scalars.all()
    return [user.serialize() for user in users]

async def register_user_by_type(session, user_model: UserModel, user_type: User.Type):
    user_model.password = str(uuid.uuid4()).split('-')[0] # random password
    user = User.from_model(user_model)
    user.user_type = user_type
    session.add(user)
    await session.commit()
