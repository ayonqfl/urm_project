from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app import db

class RolesAPI(db.Model):
    __tablename__ = 'roles_api'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    role_id = db.Column(
        db.Integer(), 
        db.ForeignKey('roles.id', ondelete='CASCADE'), 
        nullable=False
    )
    role_name = db.Column(db.String(), nullable=False)
    api = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        TIMESTAMP(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def to_dict(self):
        return {
            'id': self.id,
            'role_id': self.role_id,
            'role_name': self.role_name,
            'api': self.api,
            'type': self.type,
            'details': self.details,
            'created_at': self.created_at.strftime('%d-%m-%Y')
        }
    

# CREATE TABLE roles_api (
#     id SERIAL PRIMARY KEY,
#     role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
#     role_name VARCHAR NOT NULL
#     api VARCHAR NOT NULL,
#     type VARCHAR NOT NULL,
#     details TEXT,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
# );


# ALTER TABLE public.roles_api
# ADD COLUMN role_name VARCHAR NOT NULL