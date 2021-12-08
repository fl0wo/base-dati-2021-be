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


def check_if_space_for_slot_reservation(slotId):#TODO:fix sql injection
    sql_query = sqlalchemy.text("select * from gym.thereIsSpaceInSlotView WHERE id='"+slotId+"'")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list


def check_if_space_for_lesson_reservation(lessonId):#TODO:fix sql injection
    sql_query = sqlalchemy.text("select * from gym.thereIsSpaceInLessonView WHERE id='"+lessonId+"'")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list


def get_reservations_of(userId):#TODO:fix sql injection
    sql_query = sqlalchemy.text("select * from gym.userWithAllReservations where customer='"+userId+"'")
#"SELECT 'lesson' as reservation_type,r.id,r.date,r.time,r.customer,r.room,l.participant_number,l.reservation_id,l.lesson as slot FROM gym.reservations r RIGHT JOIN gym.lesson_reservation l on r.id = l.reservation_id WHERE r.customer='"+ userId + "' UNION ALL SELECT 'weightroom' as reservation_type,* FROM gym.reservations r RIGHT JOIN gym.weight_room_reservations on r.id = weight_room_reservations.reservation_id WHERE r.customer='"+userId +"'")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list

def get_all_lessons_curent_reservation():
    sql_query = sqlalchemy.text("select * from gym.lessons_with_current_reservation_V;")
    result = perform_query_txt(sql_query)
    result_as_list = result.fetchall()
    return result_as_list