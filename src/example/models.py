import flask_sqlalchemy
import sqlalchemy
from sqlalchemy import (Column, Integer, String, Numeric, CheckConstraint, UniqueConstraint)
from .lowdb import define_schema, define_trigger, define_roles

define_schema("gym")
define_trigger()
define_roles()

db = flask_sqlalchemy.SQLAlchemy()

ID_TYPE = db.String(36)


class Cats(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    breed = db.Column(db.String(100))


class Users(db.Model):
    __tablename__ = "users"

    __table_args__ = (UniqueConstraint("email"), {"schema": "gym"})

    id = db.Column("id", ID_TYPE, primary_key=True)  # siamo gia dentro user sappiamo che id e' id_user. ^-^
    name = db.Column("name", db.String(50), nullable=True)
    surname = db.Column("surname", db.String(50), nullable=True)
    birth_date = db.Column("birth_date", db.Date, nullable=True)
    #  fiscal code
    fiscal_code = db.Column("fiscal_code", db.String(50), nullable=True)
    phone = db.Column("phone", db.String(50), nullable=True)
    role = db.Column("role", db.String(50), nullable=True)
    email = db.Column("email", db.String(50), nullable=False)
    password = db.Column("password", db.String(1000), nullable=False)


class Subscriptions(db.Model):
    __table_name__ = "Subscriptions"
    __table_args__ = (
        CheckConstraint('end_date > start_date'),
        {"schema": "gym"}
    )

    id = db.Column("id", ID_TYPE, primary_key=True)
    start_date = db.Column("start_date", db.Date, nullable=False)
    end_date = db.Column("end_date", db.Date, nullable=False)
    cur_balance = db.Column("cur_balance", db.Numeric(15, 2), CheckConstraint("cur_balance > 0"),  nullable=False)
    user = db.Column(ID_TYPE, db.ForeignKey(Users.id), nullable=False)


class Products(db.Model):
    __table_name__ = "Products"
    __table_args__ = {"schema": "gym"}

    id = db.Column("id", ID_TYPE, primary_key=True)
    description = db.Column("description", db.String(50))
    price = db.Column("price", db.Numeric(15, 2), CheckConstraint("price > 0"))


class Transactions(db.Model):
    __table_name__ = "Transactions"
    __table_args__ = {"schema": "gym"}

    id = db.Column("id", ID_TYPE, primary_key=True)
    date = db.Column("date", db.Date)
    time = db.Column("time", db.Time)
    description = db.Column("description", db.String(50))
    subscription = db.Column("subscription", ID_TYPE, db.ForeignKey(Subscriptions.id), nullable=False)
    product = db.Column("product", ID_TYPE, db.ForeignKey(Products.id), nullable=False)


class Policies(db.Model):
    __table_name__ = "Policies"
    __table_args__ = (
        CheckConstraint('valid_to > valid_from'),
        {"schema": "gym"}
    )

    id = db.Column("id", ID_TYPE, primary_key=True)
    description = db.Column("description", db.String(50))
    valid_from = db.Column("valid_from", db.Date)
    valid_to = db.Column("valid_to", db.Date)


class Courses(db.Model):
    __table_name__ = "Courses"
    __table_args__ = {"schema": "gym"}

    id = db.Column("id", ID_TYPE, primary_key=True)
    name = db.Column("name", db.String(50))
    description = db.Column("description", db.String(50))
    trainer = db.Column("trainer", ID_TYPE, db.ForeignKey(Users.id), nullable=False)


class Accesses(db.Model):
    __table_name__ = "Accesses"
    __table_args__ = (
        CheckConstraint('time_exit > time_entrance'),
        {"schema": "gym"}
    )

    id = db.Column("id", ID_TYPE, primary_key=True)
    date = db.Column("date", db.Date)
    time_entrance = db.Column("time_entrance", db.Time)
    time_exit = db.Column("time_exit", db.Time)
    user = db.Column("user", ID_TYPE, db.ForeignKey(Users.id), nullable=False)


class Rooms(db.Model):
    __table_name__ = "Rooms"
    __table_args__ = {"schema": "gym"}

    id = db.Column("id", ID_TYPE, primary_key=True)
    description = db.Column("description", db.String(50))


class Reservations(db.Model):
    __table_name__ = "Reservations"
    __table_args__ = (
        UniqueConstraint("room", "date", "time"),
        {"schema": "gym"}
    )

    id = db.Column("id", ID_TYPE, primary_key=True)
    date = db.Column("date", db.Date)
    time = db.Column("time", db.Time)
    customer = db.Column("customer", ID_TYPE, db.ForeignKey(Users.id), nullable=False)
    room = db.Column("room", ID_TYPE, db.ForeignKey(Rooms.id), nullable=False)


class Lessons(db.Model):
    __table_name__ = "Lessons"
    __table_args__ = (
        UniqueConstraint("course", "date", "time"),
        {"schema": "gym"}
    )

    id = db.Column("id", ID_TYPE, primary_key=True)
    date = db.Column("date", db.Date)
    time = db.Column("time", db.Time)
    max_participants = db.Column("max_participants", db.Integer, CheckConstraint("max_participants > 0"), default=20)
    course = db.Column("course", ID_TYPE, db.ForeignKey(Courses.id), nullable=False)


class Slots(db.Model):
    __table_name__ = "Slots"
    __table_args__ = (
        UniqueConstraint("time_from", "time_to", "date"),
        CheckConstraint('time_to > time_from'),
        {"schema": "gym"}
    )

    id = db.Column("id", ID_TYPE, primary_key=True)
    date = db.Column("date", db.Date)
    time_from = db.Column("time_from", db.Time)
    time_to = db.Column("time_to", db.Time)
    max_capacity = db.Column("max_capacity", db.Integer, CheckConstraint("max_capacity > 0"), default=20)


class WeightRoomReservations(db.Model):
    __table_name__ = "WeightRoomReservations"
    __table_args__ = (UniqueConstraint("slot", "reservation_id"), {"schema": "gym"})

    reservation_number =  db.Column("reservation_number", db.Integer, primary_key=True)
    reservation_id = db.Column("reservation_id", ID_TYPE, db.ForeignKey(Reservations.id),
                               primary_key=True, nullable=False)
    slot = db.Column("slot", ID_TYPE, db.ForeignKey(Slots.id), nullable=False)


class LessonReservation(db.Model):
    __table_name__ = "LessonReservation"
    __table_args__ = (UniqueConstraint("lesson", "reservation_id"), {"schema": "gym"})

    participant_number = db.Column("participant_number", db.Integer, primary_key=True)
    reservation_id = db.Column("reservation_id", ID_TYPE, db.ForeignKey("gym.reservations.id"),
                               primary_key=True, nullable=False)
    lesson = db.Column("lesson", ID_TYPE, db.ForeignKey(Lessons.id), nullable=False)

