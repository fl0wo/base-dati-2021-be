import flask_sqlalchemy
from sqlalchemy import UniqueConstraint

db = flask_sqlalchemy.SQLAlchemy()


class Cats(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    breed = db.Column(db.String(100))


class Users(db.Model):
    __tablename__ = "users"

    __table_args__ = (UniqueConstraint("email"), {"schema": "gym"})

    id = db.Column("id", db.String(100), primary_key=True)  # siamo gia dentro user sappiamo che id e' id_user.
    name = db.Column("name", db.String(50), nullable=True)
    surname = db.Column("surname", db.String(50), nullable=True)
    birth_date = db.Column("birth_date", db.Date, nullable=True)
    #  fiscal code
    fiscal_code = db.Column("fiscal_code", db.String(50), nullable=True)
    phone = db.Column("phone", db.String(50), nullable=True)
    role = db.Column("role", db.String(50), nullable=True)
    email = db.Column("email", db.String(50), nullable=False)
    password = db.Column("password", db.String(100), nullable=False)


