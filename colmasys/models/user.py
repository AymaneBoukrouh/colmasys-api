from colmasys import auth
from colmasys.models import Model
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, Date, Boolean
from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    firstname: str
    lastname: str
    username: str | None
    email: str
    password: str | None
    birthdate: str
    gender: bool
    user_type: int


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
        return User(
            firstname = user.firstname,
            lastname = user.lastname,
            username = user.username,
            email = user.email,
            password = auth.hash_password(user.password),
            birthdate = datetime.strptime(user.birthdate, '%d/%m/%Y'),
            gender = user.gender,
            user_type = user.user_type
        )

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
