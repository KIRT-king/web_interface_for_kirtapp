from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from web_interface_for_kirtapp.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    post = Column(String(150))
    email = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(20))
    status = Column(String(100), nullable=False)
    last_check = Column(String(50), nullable=False)

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")


class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("admins.id"))
    user = relationship("Admin")