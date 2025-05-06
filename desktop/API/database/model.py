from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Licences(Base):
    __tablename__ = "licences"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, default=365)
    created_at = Column(DateTime, default=datetime.utcnow)


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default='Not name', index=True)
    director = Column(String, index=True)
    phone = Column(String(11))
    license = Column(Integer, ForeignKey('licences.id'))


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default='Not name', index=True)
    company = Column(Integer, ForeignKey('company.id'))
    role = Column(Integer, ForeignKey('roles.id'))
    login = Column(String, unique=True)
    password = Column(String) 


class FileStorage(Base):
    __tablename__ = "filestorage"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    duration = Column(String, default='00:00:00')
    size = Column(String, default='0 bytes')
    text_data = Column(String)


class Lessons(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    file = Column(Integer, ForeignKey('filestorage.id'))
    mark = Column(Integer, default=100)


class VideoAudioAnalyz(Base):
    __tablename__ = "videoaudioanalyz"
    id = Column(Integer, primary_key=True, index=True)
    lid = Column(Integer, ForeignKey('lessons.id'))
    video = Column(String)
    audio = Column(String)