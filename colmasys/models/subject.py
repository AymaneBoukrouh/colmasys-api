from colmasys.models import Model
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class SubjectModel(BaseModel):
    id: int
    name: str

class Subject(Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    _professors_and_classes = relationship('ProfessorClass', backref='subject')

    @property
    def professors(self):
        return [pc.professor for pc in self._professors_and_classes]
    
    @property
    def classes(self):
        return [pc.class_ for pc in self._professors_and_classes]

    @staticmethod
    def from_model(subject_model: SubjectModel):
        return Subject(**subject_model.dict())

    def serialize(self):
        return {'id': self.id, 'name': self.name}


class ProfessorClassModel(BaseModel):
    id: int
    professor_id: int
    class_id: int
    subject_id: int

class ProfessorClass(Model):
    __tablename__ = 'professor_class'
    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('professor.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
