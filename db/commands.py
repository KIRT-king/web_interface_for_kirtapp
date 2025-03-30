import secrets
from typing import Optional

from db.database import Session
from db.models import Admin, SessionModel, User


def get_user_by_username(username: str):
    with Session() as session:
        return session.query(Admin).filter(Admin.username == username).first()

def create_session(user_id: int):
    with Session() as session:
        existing_session = session.query(SessionModel).filter(SessionModel.user_id == user_id).first()
        session_id = secrets.token_hex(16)
        if existing_session:
            existing_session.session_id = session_id
            session.commit()
            return existing_session.session_id
        else:
            new_session = SessionModel(session_id=session_id, user_id=user_id)
            session.add(new_session)
            session.commit()
            return new_session.session_id

def get_user_by_session(session_id: str):
    with Session() as session:
        session_cookie = session.query(SessionModel).filter(SessionModel.session_id == session_id).first()
        return session_cookie.user if session_cookie else None

def delete_session(session_id: str):
    with Session() as session:
        session.query(SessionModel).filter(SessionModel.session_id == session_id).delete()
        session.commit()

def get_latest_users_commands(limit: int):
    with Session() as session:
        users = session.query(User).order_by(User.id).limit(limit).all()
        return users

def search_users_commands(name: Optional[str] = None,
                          phone_number: Optional[str] = None,
                          email: Optional[str] = None):
    with Session() as session:
        query = session.query(User)

        conditions = []
        if name:
            conditions.append(User.name.ilike(f"%{name}%"))
        if phone_number:
            conditions.append(User.phone_number == phone_number)
        if email:
            conditions.append(User.email == email)

        if conditions:
            query = query.filter(*conditions)

        return query.all()
