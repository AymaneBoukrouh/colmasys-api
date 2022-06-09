from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base(name='Model')

from colmasys.models.account import *
from colmasys.models.professor import *
from colmasys.models.student import *
from colmasys.models.class_ import *
from colmasys.models.subject import *