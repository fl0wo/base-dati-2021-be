from .models import db
import sqlalchemy
from .lowdb import perform_query_txt

def get_all(model):
    data = model.query.all()
    return data


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()

def add_instance_no_commit(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)

def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()


def get_by_id(model, id):
    data = model.query.filter_by(id=id).first()
    return data


def get_by_email(model, email):
    data = model.query.filter_by(email=email).first()
    return data

def begin_transaction():
    db.session.begin()

def commit_changes():
    db.session.commit()

def get_all_slots_curent_reservation():
    sql_query = sqlalchemy.text("SELECT s.*, count(w.*) as current_reservations FROM gym.slots s left join gym.weight_room_reservations w on s.id = w.slot group by id, date, time_from, time_to, max_capacity;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list;

def check_if_space_for_slot_reservation(slotId):
    sql_query = sqlalchemy.text("SELECT 1 as there_is_space FROM(SELECT s.*, count(w.*) as current_reservations FROM gym.slots s left join gym.weight_room_reservations w on s.id = w.slot where s.id = '"+slotId+"' group by id, date, time_from, time_to, max_capacity) as slotReservations where max_capacity>current_reservations UNION  ALL SELECT 0 LIMIT  1;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list;