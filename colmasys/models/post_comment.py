from colmasys.models import Model
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime


class CommentModel(BaseModel):
    content: str | None

class PostModel(CommentModel):
    title: str | None


class UserContent(Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    content = Column(String(2048), nullable=False)
    creation_datetime = Column(DateTime, default=datetime.utcnow)
    deletion_datetime = Column(DateTime, nullable=True)
    deleted = Column(Boolean, default=False)

    def update_from_model(self, model):
        data = model.dict()
        for attr in data.keys():
            if (value:=data[attr]):
                setattr(self, attr, value)
    
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'creation_datetime': self.creation_datetime.strftime('%d/%M/%Y %H:%M:%S'),
            'author': self.author.serialize()
        }


class Comment(UserContent):
    __tablename__ = 'comment'

    author_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    @staticmethod
    def from_model(model: CommentModel):
        return Comment(**model.dict())


class Post(UserContent):
    __tablename__ = 'post'

    title = Column(String(256))
    author_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    comments = relationship('Comment', backref=backref('post', lazy='selectin'), lazy='selectin')

    @staticmethod
    def from_model(model: PostModel):
        return Post(**model.dict())

    def serialize(self):
        data = super().serialize()
        data.update({'title': self.title})
        return data
