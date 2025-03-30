from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
connection_path = os.path.join(script_dir, "web_interface_for_kirtapp", "connection.txt")

with open(connection_path, "r") as file:
    connection_string = file.read()

engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
Base = declarative_base()
