from colmasys.models import Model
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime


class VoteModel(BaseModel):
    value: bool
  

class Vote(Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    value = Column(Boolean, nullable=False)
    deleted = Column(Boolean, default=False)


class CommentVote(Vote):
    __tablename__ = 'comment_vote'

    account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    comment_id = Column(Integer, ForeignKey('comment.id', ondelete='CASCADE'), nullable=False)

    @staticmethod
    def from_model(model: VoteModel):
        return CommentVote(**model.dict())

    def serialize(self):
        return {
            'id': self.id,
            'value': self.value
        }

  
class PostVote(Vote):
    __tablename__ = 'post_vote'

    account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    @staticmethod
    def from_model(model: VoteModel):
        return PostVote(**model.dict())
    
    def serialize(self):
        return {
            'id': self.id,
            'value': self.value
        }
