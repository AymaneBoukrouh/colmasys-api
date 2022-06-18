from colmasys.models import Professor, Student, Account, AccountModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid

async def account_filter_by_scalars(session, **kwargs):
    query = (
            select(Account)
            .filter_by(**kwargs)
        )
    
    result = await session.execute(query)
    return result.scalars()

async def get_account_by(session, **kwargs):
    scalars = await account_filter_by_scalars(session, **kwargs)
    return scalars.first()

async def get_accounts_by_type(session, account_type):
    users = (await session.execute(select(account_type))).scalars().all()
    return [user.account.serialize() for user in users]

async def get_students(session):
    return await get_accounts_by_type(session, Student)

async def get_professors(session):
    return await get_accounts_by_type(session, Professor)

async def register_account_by_type(session, account_model: AccountModel, account_type: Account.Type):
    account_model.password = str(uuid.uuid4()).split('-')[0] # random password
    account = Account.from_model(account_model)
    account.account_type = account_type
    session.add(account)

    if account_type == Account.Type.Professor:
        user = Professor(account=account)
    elif account_type == Account.Type.Student:
        user = Student(account=account)
    
    session.add(user)
    await session.commit()

async def register_student(session, account_model):
    await register_account_by_type(session, account_model, Account.Type.Student)

async def register_professor(session, account_model):
    await register_account_by_type(session, account_model, Account.Type.Professor)
