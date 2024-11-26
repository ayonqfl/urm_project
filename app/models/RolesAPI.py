from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app import db

class RolesAPI(db.Model):
    __tablename__ = 'roles_api'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    role_id = user_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
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
            'role_id': self.role_id,
            'role_name': self.role_name,
            'api': self.api,
            'type': self.type,
            'details': self.details,
        }
    

# CREATE TABLE roles_api (
#     id SERIAL PRIMARY KEY,
#     role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
#     api VARCHAR NOT NULL,
#     type VARCHAR NOT NULL,
#     details TEXT,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
# );
