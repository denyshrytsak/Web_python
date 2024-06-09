from sqlalchemy import Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
from app import db, bcrypt

class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[date] = mapped_column(Date, nullable=True) 
    complete: Mapped[bool] = mapped_column(Boolean)

class Feedback(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_email: Mapped[str] = mapped_column(String)
    topic: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    mark: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime) 

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.jpg')
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    
    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    @property
    def password(self):
        return AttributeError("Password is not readable!!")

    @password.setter
    def password(self, value):
        self.password_hash = bcrypt.generate_password_hash(value)

    def verify_password(self, value):
        return bcrypt.check_password_hash(self.password_hash, value)
    
    def __repr__(self) -> str:
        return f"User({self.username}, {self.email})"