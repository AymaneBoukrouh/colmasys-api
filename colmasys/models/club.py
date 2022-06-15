from colmasys.models import Model
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime


class ClubMember(Model):
    __tablename__ = 'club_member'

    club = Column(Integer, ForeignKey('club.id'), primary_key=True)
    student = Column(Integer, ForeignKey('student.id'), primary_key=True)
    join_datetime = Column(DateTime, default=datetime.utcnow)

class ClubStaff(Model):
    __tablename__ = 'club_staff'

    club = Column(Integer, ForeignKey('club.id'), primary_key=True)
    student = Column(Integer, ForeignKey('student.id'), primary_key=True)
    join_datetime = Column(DateTime, default=datetime.utcnow)
    role = Column(String(64), nullable=False)


class ClubModel(BaseModel):
    name: str    


class Club(Model):
    __tablename__ = 'club'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    deletion_datetime = Column(DateTime, nullable=True)

    staff = relationship('Student', secondary='club_staff', backref=backref('clubs_staff', lazy='selectin'), lazy='selectin')
    members = relationship('Student', secondary='club_member', backref=backref('clubs_member', lazy='selectin'), lazy='selectin')

    @staticmethod
    def from_model(club_model: ClubModel):
        return Club(**club_model.dict())

    def update_from_model(self, club_model: ClubModel):
        data = club_model.dict()
        for attr in data.keys():
            setattr(self, attr, data[attr])

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
