from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TIMESTAMP
from flask_login import UserMixin

from app import db

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    type = db.Column(db.Enum('Admin', 'API', name='user_types'), nullable=False)
    email = db.Column(db.String(), nullable=True, unique=True)
    phone = db.Column(db.String(), nullable=True, unique=True)
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

    # users_role = db.relationship(
    #     'UsersRole', 
    #     backref='usersrole', 
    #     cascade='all, delete-orphan'
    # )

    def __repr__(self):
        return f"<User {self.username}>"
    

# SQL create table scripts
# CREATE TYPE user_types AS ENUM ('Admin', 'API');

# CREATE TABLE users (
#     id SERIAL PRIMARY KEY,
#     username VARCHAR NOT NULL UNIQUE,
#     email VARCHAR NULL UNIQUE,
#     phone VARCHAR NULL UNIQUE;
#     password VARCHAR NOT NULL,
#     api_token VARCHAR UNIQUE,
#     type user_types NOT NULL,
#     details TEXT,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
#     updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
# );