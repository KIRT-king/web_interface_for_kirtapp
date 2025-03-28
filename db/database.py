from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

with open("connection.txt", "r") as file:
    connection_string = file.read()

engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
Base = declarative_base()
