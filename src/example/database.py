from .models import db, Accesses, Policies
import sqlalchemy
from .lowdb import perform_query_txt
from sqlalchemy import bindparam, String
from datetime import datetime, timedelta


def begin_transaction():
    db.session.begin()

def commit_changes():
    db.session.commit()

def rollback_changes():
    db.session.rollback()

def get_all(model):
    data = model.query.all()
    return data


def add_instance(model, **kwargs):
    try:
        #begin_transaction()
        instance = model(**kwargs)
        db.session.add(instance)
        commit_changes()
    except Exception as e:
        rollback_changes()
        print(e)
        raise e


def delete_instance(model, id):
    try:
        begin_transaction()
        model.query.filter_by(id=id).delete()
        commit_changes()
    except:
        rollback_changes()


def flush():
    db.session.flush()


def add_instance_no_commit(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).first()
    for attr, new_value in kwargs.items():
        if new_value is not None:
            setattr(instance, attr, new_value)
    commit_changes()


def get_by_id(model, id):
    data = model.query.filter_by(id=id).first()
    return data

def get_by_role(model, role):
    data = model.query.filter_by(role=role).all()
    return data


def get_by_email(model, email):
    data = model.query.filter_by(email=email).first()
    return data


def get_all_slots_curent_reservation():
    sql_query = sqlalchemy.text("select * from gym.slots_with_current_reservation_V;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list


def check_if_space_for_slot_reservation(slotId):
    sql_query = sqlalchemy.text("select * from gym.there_Is_Space_In_Slot_View WHERE id=:slotId")
    sql_query = sql_query.bindparams(bindparam('slotId', value=slotId, type_=String))
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list


def check_if_space_for_lesson_reservation(lessonId):
    sql_query = sqlalchemy.text("select * from gym.there_Is_Space_In_Lesson_View WHERE id=:lessonId")
    sql_query = sql_query.bindparams(bindparam('lessonId', value=lessonId, type_=String))
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list


def get_reservations_of(userId):
    sql_query = sqlalchemy.text("select * from gym.user_With_All_Reservations where customer=:userId")
    sql_query = sql_query.bindparams(bindparam('userId', value=userId, type_=String))
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list

def get_all_lessons_curent_reservation():
    sql_query = sqlalchemy.text("select * from gym.lessons_with_current_reservation_V;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list

def get_all_accesses(userId):
    data = Accesses.query.filter_by(user=userId).all()
    return data

def get_current_policy():
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    data = Policies.query.filter(todays_datetime < Policies.valid_to).all()
    return data
