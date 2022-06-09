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

async def get_accounts_by_type(session, account_type: Account.Type):
    scalars = await account_filter_by_scalars(session, account_type=account_type)
    accounts = scalars.all()
    return [account.serialize() for account in accounts]

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
