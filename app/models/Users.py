from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TIMESTAMP
from flask_login import UserMixin

from app import db

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    api_token = db.Column(db.String(256), nullable=True, unique=True)
    type = db.Column(db.Enum('Admin', 'API', name='user_types'), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        TIMESTAMP(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = db.Column(
        TIMESTAMP(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def __repr__(self):
        return f"<User {self.username}>"
    

# SQL create table scripts
# CREATE TYPE user_types AS ENUM ('Admin', 'API');

# CREATE TABLE users (
#     id SERIAL PRIMARY KEY,
#     username VARCHAR NOT NULL UNIQUE,
#     email VARCHAR NOT NULL UNIQUE,
#     password VARCHAR NOT NULL,
#     api_token VARCHAR UNIQUE,
#     type user_types NOT NULL,
#     details TEXT,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
#     updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
# );