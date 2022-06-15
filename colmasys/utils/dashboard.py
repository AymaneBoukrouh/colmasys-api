from colmasys.models import Model
from sqlalchemy import func, select

async def number_of_rows(session, model: Model) -> int:
    '''return number of rows of a model'''
    return (await session.execute(select(func.count(model.id)))).scalar_one()