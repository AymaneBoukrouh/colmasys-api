from colmasys import auth
from colmasys.models import Model
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, DateTime, Date, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime


class Student(Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    account = relationship(
        'Account', uselist=False, lazy='selectin',
        backref = backref('student', uselist=False, lazy='selectin')
    )

    class_id = Column(Integer, ForeignKey('class.id', ondelete='CASCADE'), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'account': self.account.serialize(),
            'class': self.class_.serialize()
        }
