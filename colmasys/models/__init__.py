from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base(name='Model')

from colmasys.models.user import *
from colmasys.models.class_ import *
from colmasys.models.module_subject import *