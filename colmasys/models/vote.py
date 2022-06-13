from colmasys.models import Model
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime
from abc import ABC


class VoteModel(BaseModel, ABC):
    value: bool

class CommentVoteModel(VoteModel):
    comment_id: int

class PostVoteModel(VoteModel):
    post_id: int

  
class Vote(Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    value = Column(Boolean, nullable=False)
    deleted = Column(Boolean, default=False)


class CommentVote(Vote):
    __tablename__ = 'comment_vote'
    comment_id = Column(Integer, ForeignKey('comment.id', ondelete='CASCADE'), nullable=False)

    @staticmethod
    def from_model(model: CommentVoteModel):
        return CommentVote(**model.dict())

  
class PostVote(Vote):
    __tablename__ = 'post_vote'
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    @staticmethod
    def from_model(model: PostVoteModel):
        return PostVote(**model.dict())
