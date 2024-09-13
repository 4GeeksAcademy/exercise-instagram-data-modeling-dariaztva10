import os
import sys
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

# Crear la base declarativa para los modelos
Base = declarative_base()


# Definir el Enum para el tipo de media
class MyEnum(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class Follower(Base):
    __tablename__ = "follower"
    user_from_id =  Column(Integer, ForeignKey('user.id'), primary_key=True) 
    user_to_id =  Column(Integer, ForeignKey('user.id'), primary_key=True)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True) #Define una columna id que es una clave primaria de tipo entero.
    username =  Column(String(250), nullable=False, unique=True) #Define una columna de tipo cadena, máx 250 carcateres, que no puede ser nula
    firstname =  Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

    comments = relationship('Comment', back_populates='user', lazy=True) 
    posts = relationship('Post', back_populates='user', lazy=True) 
    following = relationship('Follower', foreign_keys=[Follower.user_from_id], back_populates='following')
    followers = relationship('Follower', foreign_keys=[Follower.user_to_id],back_populates='followers')

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id =  Column(Integer, ForeignKey('user.id'),  nullable=False)
    post_id =  Column(Integer, ForeignKey('post.id'), nullable=False)

    
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer, ForeignKey('user.id'), nullable=False) 

    comments = relationship('Comment', back_populates='post', lazy=True) 
    media = relationship('Media', back_populates='post', lazy=True) 

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(MyEnum), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'),  nullable=False)


    def to_dict(self):
        return {}
    
#CREANDO LA BASE DE DATOS SQLite
engine = create_engine('sqlite:///test.db')

#CREANDO LAS TABLAS EN LA BASE DE DATOS
Base.metadata.create_all(engine)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! Revisa el archivo diagram.png :)")
except Exception as e:
    print("Hubo un problema al generar el diagrama :(")
    raise e
