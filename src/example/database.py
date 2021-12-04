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
    instance = model.query.filter_by(id=id).first()
    for attr, new_value in kwargs.items():
        if new_value is not None:
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
    sql_query = sqlalchemy.text("select * from gym.slots_with_current_reservation_V;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list


def check_if_space_for_slot_reservation(slotId):
    sql_query = sqlalchemy.text("SELECT 1 as there_is_space FROM(SELECT s.*, count(w.*) as current_reservations FROM gym.slots s left join gym.weight_room_reservations w on s.id = w.slot where s.id = '"+slotId+"' group by id, date, time_from, time_to, max_capacity) as slotReservations where max_capacity>current_reservations UNION  ALL SELECT 0 LIMIT  1;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list


def get_reservations_of(userId):
    sql_query = sqlalchemy.text("SELECT 'lesson' as reservation_type,r.id,r.date,r.time,r.customer,r.room,l.participant_number,l.reservation_id,l.lesson as slot FROM gym.reservations r RIGHT JOIN gym.lesson_reservation l on r.id = l.reservation_id WHERE r.customer='"+ userId + "' UNION ALL SELECT 'weightroom' as reservation_type,* FROM gym.reservations r RIGHT JOIN gym.weight_room_reservations on r.id = weight_room_reservations.reservation_id WHERE r.customer='"+userId +"'")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list

def get_all_lessons_curent_reservation():
    sql_query = sqlalchemy.text("SELECT l.id, l.date, l.time, l.max_participants, count(lr.*) as current_reservations, c.name as course, c.description as course_description FROM gym.lessons l left join gym.lesson_reservation lr on l.id = lr.lesson inner join gym.courses c on c.id = l.course group by l.id, date, time, max_participants, c.name, c.description;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list