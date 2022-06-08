from colmasys import auth
from colmasys.models import Model
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, DateTime, Date, Boolean
from sqlalchemy.orm import relationship
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
    class_id = Column(Integer, ForeignKey('class.id'), nullable=True)
    
    _professors_and_classes = relationship('ProfessorClass', backref='professor')

    @property
    def professors(self):
        return [pc.professor for pc in self._professors_and_classes]
    
    @property
    def classes(self):
        return [pc.class_ for pc in self._professors_and_classes]

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
