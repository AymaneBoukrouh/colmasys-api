from colmasys import auth
from colmasys.models import Model
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, DateTime, Date, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime


class AccountModel(BaseModel):
    firstname: str
    lastname: str
    username: str | None
    email: str
    password: str | None
    birthdate: str
    gender: bool


class Account(Model):
    class Type:
        Admin = 0
        Student = 1
        Professor = 2

    class Gender:
        male = 0
        female = 1

    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    birthdate = Column(Date, nullable=True)
    gender = Column(Boolean, nullable=False)
    account_type = Column(SmallInteger, nullable=False)
    creation_datetime = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    deletion_datetime = Column(DateTime, nullable=True)

    professor_id = Column(Integer, ForeignKey('professor.id', ondelete='CASCADE'), nullable=True)
    student_id = Column(Integer, ForeignKey('student.id', ondelete='CASCADE'), nullable=True)

    posts = relationship('Post', backref=backref('author', lazy='selectin'), lazy='selectin')
    comments = relationship('Comment', backref=backref('author', lazy='selectin'), lazy='selectin')
    
    post_votes = relationship('PostVote', backref=backref('account', lazy='selectin'), lazy='selectin')
    comment_votes = relationship('CommentVote', backref=backref('account', lazy='selectin'), lazy='selectin')

    messages = relationship('Message', backref=backref('author', lazy='selectin'), lazy='selectin')

    @property
    def user(self):
        users = [self.professor, self.student]
        for user in users:
            if user:
                return user

    @property
    def private_chats(self):
        return [chat for chat in self.chats if not chat.group]

    @property
    def group_chats(self):
        return [chat for chat in self.chats if chat.group]

    @staticmethod
    def from_model(model: AccountModel):
        data = model.dict()
        data['password'] = auth.hash_password(model.password)
        data['birthdate'] = datetime.strptime(model.birthdate, '%d/%m/%Y')
        return Account(**data)

    def update_from_model(self, model: AccountModel):
        data = model.dict()
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
