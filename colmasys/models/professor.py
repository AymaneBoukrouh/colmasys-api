from colmasys.models import Model
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, backref


class Professor(Model):
    __tablename__ = 'professor'
    id = Column(Integer, primary_key=True)

    account = relationship(
        'Account', uselist=False, lazy='selectin',
        backref = backref('professor', uselist=False, lazy='selectin')
    )
    _pcs = relationship('ProfessorClassSubject', backref=backref('professor', lazy='selectin'), lazy='selectin')

    @property
    def classes(self):
        return [pcs.class_ for pcs in self._pcs]

    @property
    def subjects(self):
        return [pcs.subject for pcs in self._pcs]

    def serialize(self):
        data = {
            'id': self.id,
            'number_of_classes': len(self.classes),
            'number_of_subjects': len(self.subjects)
        }

        data.update(self.account.serialize())
        return data
