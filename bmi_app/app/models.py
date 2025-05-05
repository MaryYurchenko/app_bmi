from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # Импортируем Base из database.py


class User(Base):
    __tablename__ = "users"  # Обязательно указываем имя таблицы

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False)
    records = relationship("BMIRecord", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"  # Имя таблицы

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")


class BMIRecord(Base):
    __tablename__ = "bmi_records"  # Имя таблицы

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight = Column(Float, nullable=False)   # кг
    height = Column(Float, nullable=False)   # м
    bmi = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="records")