from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app import db

class UsersRole(db.Model):
    __tablename__ = 'users_role'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    role_id = db.Column(
        db.Integer(),
        db.ForeignKey('roles.id', ondelete='CASCADE'),
        nullable=False
    )
    username = db.Column(db.String(), nullable=False)
    role_name = db.Column(db.String(), nullable=False)

    user = db.relationship('Users', backref='user_roles', lazy='joined')
    role = db.relationship('Roles', backref='user_roles', lazy='joined')

    created_at = db.Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


# CREATE TABLE users_role (
#     id SERIAL PRIMARY KEY,
#     user_id INTEGER NOT NULL,
#     role_id INTEGER NOT NULL,
#     username VARCHAR NOT NULL,
#     role_name VARCHAR NOT NULL,
#     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
#     CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
#     CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
# );

# -- Optionally, create an index on user_id and role_id for faster lookups
# CREATE INDEX idx_users_role_user_id ON users_role(user_id);
# CREATE INDEX idx_users_role_role_id ON users_role(role_id);
