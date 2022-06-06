from colmasys.models import Model, User
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class ClassModel(BaseModel):
    academic_year: str
    year: int
    group: int
    major: str


class Class(Model):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    academic_year = Column(String(9), nullable=False)
    year = Column(Integer, nullable=False)
    group = Column(Integer, nullable=False)
    major = Column(String(32), nullable=False)
    deleted = Column(Boolean, default=False)
    deletion_datetime = Column(DateTime, nullable=True)

    _students = relationship('User', backref='class_', lazy='selectin')

    @property
    def students(self):
        return [student.serialize() for student in self._students]

    @staticmethod
    def from_model(class_model: ClassModel):
        return Class(**class_model.dict())

    def update_from_model(self, class_model: ClassModel):
        data = class_model.dict()
        for attr in data.keys():
            setattr(self, attr, data[attr])

    def serialize(self):
        return {
            'id': self.id,
            'academic_year': self.academic_year,
            'year': self.year,
            'group': self.group,
            'major': self.major
        }
