from colmasys import auth
from colmasys.models import Model, AccountModel
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, DateTime, Date, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime


class StudentModel(AccountModel):
    class_id: int | None


class Student(Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    account = relationship(
        'Account', uselist=False, lazy='selectin',
        backref = backref('student', uselist=False, lazy='selectin')
    )

    class_id = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'), nullable=True)

    @property
    def clubs(self):
        return self.clubs_staff + self.clubs_member

    def serialize(self):
        data = {
            'id': self.id,
            'class_id': self.class_id,
            'class': self.class_.name if self.class_ else ''
        }

        data.update(self.account.serialize())
        return data
