from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='posts')

engine = create_engine("mysql+mysqlconnector://root:12345@localhost/db", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

print("Таблицы успешно созданы!")
