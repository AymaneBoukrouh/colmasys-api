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

    @property
    def n_votes(self):
        votes = [vote.value for vote in self.votes if not vote.deleted]
        return 2*sum(votes) - len(votes)

    def update_from_model(self, model):
        data = model.dict()
        for attr in data.keys():
            if (value:=data[attr]):
                setattr(self, attr, value)
    
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'creation_datetime': self.creation_datetime.strftime('%d/%m/%Y %H:%M:%S'),
            'author': self.author.fullname
        }


class Comment(UserContent):
    __tablename__ = 'comment'

    author_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    votes = relationship('CommentVote', backref=backref('comment', lazy='selectin'), lazy='selectin')

    @staticmethod
    def from_model(model: CommentModel):
        return Comment(**model.dict())

    def serialize(self):
        data = super().serialize()
        data.update({
            'n_votes': self.n_votes
        })

        return data


class Post(UserContent):
    __tablename__ = 'post'

    title = Column(String(256))
    author_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    comments = relationship('Comment', backref=backref('post', lazy='selectin'), lazy='selectin')
    votes = relationship('PostVote', backref=backref('post', lazy='selectin'), lazy='selectin')

    def get_user_vote(self, user_id: int) -> bool:
        for vote in self.votes:
            if vote.account_id == user_id:
                return not vote.value
    
    @property
    def n_comments(self):
        return len([comment for comment in self.comments if not comment.deleted])

    @staticmethod
    def from_model(model: PostModel):
        return Post(**model.dict())

    def serialize(self):
        data = super().serialize()
        data.update({
            'title': self.title,
            'comments': [comment.serialize() for comment in self.comments if not comment.deleted],
            'n_comments': self.n_comments,
            'n_votes': self.n_votes,
            'current_user_vote': None
        })

        return data
