from colmasys import auth
from colmasys.models import Model
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, Date, Boolean
from pydantic import BaseModel
from datetime import datetime


class UserByModel(BaseModel):
    id: int | None
    username: str | None
    email: str | None

    def error(self) -> bool:
        args = [self.id, self.username, self.email]
        valid_args = sum(list(map(lambda x: x is not None, args)))

        if valid_args == 0:
            error_message = 'Arguments Required'
        elif valid_args > 1:
            error_message = 'Too Many Arguments'
        else:
            return
        return error_message

    @property
    def data(self):
        if self.id:
            return {'id': self.id}
        elif self.username:
            return {'username': self.username}
        elif self.email:
            return {'email': self.email}


class UserModel(BaseModel):
    firstname: str
    lastname: str
    username: str | None
    email: str
    password: str | None
    birthdate: str
    gender: bool


class User(Model):
    class Type:
        admin = 0
        student = 1
        professor = 2

    class Gender:
        male = 0
        female = 1

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    birthdate = Column(Date, nullable=True)
    gender = Column(Boolean, nullable=False)
    user_type = Column(SmallInteger, nullable=False)
    creation_datetime = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    deletion_datetime = Column(DateTime, nullable=True)

    @staticmethod
    def from_model(user: UserModel):
        data = user.dict()
        data['password'] = auth.hash_password(user.password)
        data['birthdate'] = datetime.strptime(user.birthdate, '%d/%m/%Y')
        return User(**data)

    def update_from_model(self, user: UserModel):
        data = user.dict()
        for attr in data.keys():
            if attr == 'password':
                pass # password shouldn't be updated directly.
            elif attr == 'birthdate':
                setattr(self, attr, datetime.strptime(data[attr], '%d/%m/%Y'))
            else:
                setattr(self, attr, data[attr])

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email,
            'birthdate': self.birthdate.strftime('%d/%m/%Y'),
            'gender': 'Female' if self.gender else 'Male'
        }
