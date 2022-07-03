import os
import uuid
from hashlib import md5

import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

PG_DSN = os.getenv('PG_DSN', 'postgresql://admin:1234@localhost:5432/lesson')
engine = sq.create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.Integer, primary_key=True)
    email = sq.Column(sq.String(50), nullable=False, unique=True)
    password = sq.Column(sq.String(100), nullable=False)
    advs = relationship('AdvModel', back_populates='owner')

    @classmethod
    def register(cls, session: Session, email: str, password: str):
        new_user = UserModel(
            email=email,
            password=str(md5(password.encode()).hexdigest())
        )
        session.add(new_user)
        try:
            session.commit()
            return new_user
        except IntegrityError:
            session.rollback()

    def check_password(self, password: str):
        return md5(password.encode()).hexdigest() == self.password

    def to_dict(self):
        return {'id': self.id,
                'email': self.email,
                'password hash': self.password}


class Token(Base):
    __tablename__ = 'tokens'
    id = sq.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    creation_time = sq.Column(sq.DateTime, server_default=sq.func.now())
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"))
    user = relationship(UserModel, lazy="joined")


class AdvModel(Base):
    __tablename__ = 'advs'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(100), nullable=False)
    description = sq.Column(sq.String(500), nullable=False)
    creation_date = sq.Column(sq.Date(), server_default=sq.func.current_date())
    owner_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
    owner = relationship(UserModel, lazy="joined", back_populates='advs')

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'creation_date': self.creation_date,
                'owner_id': self.owner_id}


Base.metadata.create_all(engine)
