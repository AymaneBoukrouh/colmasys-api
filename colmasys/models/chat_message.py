from colmasys.models import Model
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from datetime import datetime


account_chat = Table(
    'account_chat',
    Model.metadata,
    Column('account', ForeignKey('account.id'), primary_key=True),
    Column('chat', ForeignKey('chat.id'), primary_key=True)
)


class MessageModel(BaseModel):
    content: str


class Chat(Model):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True)
    group = Column(Boolean, default=False)
    creation_datetime = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    deletion_datetime = Column(DateTime, nullable=True)

    messages = relationship('Message', backref=backref('chat', lazy='selectin'), lazy='selectin')
    accounts = relationship('Account', secondary='account_chat', backref=backref('chats', lazy='selectin'), lazy='selectin')

    def serialize(self):
        return {
            'id': self.id,
            'group_chat': self.group_chat,
            'creation_datetime': self.creation_datetime.strftime('%d/%M/%Y %H:%M:%S')
        }


class Message(Model):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    content = Column(String(2048), nullable=False)
    creation_datetime = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    deletion_datetime = Column(DateTime, nullable=True)

    author_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)

    @staticmethod
    def from_model(message_model: MessageModel):
        return Message(**message_model.dict())

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'author': self.author
        }
