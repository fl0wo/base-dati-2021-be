from ..models import Users, Lessons, Slots, Courses
from .. import app, database
from datetime import datetime
from ..response import Response, DATE_FORMAT, DATE_FORMAT_IN, TIME_FORMAT
import uuid

from ..utils.dateutils import format_date, format_time


def parse_slots():
    db_slots = database.get_all_slots_curent_reservation()
    slots = []
    for slot in db_slots:
        slots.append({
            "id": slot['id'],
            "date": format_date(slot['date']),
            "time_from": format_time(slot['time_from']),
            "time_to": format_time(slot['time_to']),
            "max_capacity": slot['max_capacity'],
            "current_reservations": slot['current_reservations'],
            "title": slot['title'],
            "description": slot['description']
        })
    return slots


def add_slot(request):
    body = request.get_json()
    # TODO: check that timefrom < timeto
    database.add_instance(Slots,
                          id=str(uuid.uuid4()),
                          date=body['date'],
                          time_from=body['time_from'],
                          time_to=body['time_to'],
                          max_capacity=body['max_capacity'],  # TODO: check if > 1
                          title=body['title'],
                          description=body['description'],
                          )

def add_lesson(request):
    body = request.get_json()
    # TODO: check that timefrom < timeto
    database.add_instance(Lessons,
                          id=str(uuid.uuid4()),
                          date=body['date'],
                          time=body['time'],
                          max_participants=body['max_participants'],  # TODO: check if > 1
                          course=body['course']
                          )

def add_course(request):
    body = request.get_json()
    # TODO: check that timefrom < timeto
    database.add_instance(Courses,
                          id=str(uuid.uuid4()),
                          name=body['name'],
                          description=body['description'],
                          trainer=body['trainer']
                          )


def add_slot_reservation(user, request):
    body = request.get_json()
    # database.begin_transaction() ---> sqlalchemy.exc.InvalidRequestError: A transaction is already begun on this Session.
    # TODO Cercare di capire come evitare sql injections, o facciamo dei controlli sul parametro oppure bisogna cambiare modo di fare le query
    db_is_space = database.check_if_space_for_slot_reservation(body['idSlot'])
    is_space = db_is_space[0]['there_is_space']  # TODO IVAN Controlla se sta roba funziona
    if is_space == 0:
        return sendResponse({}, "Not enough space in slot", 401)

    reservation_id = str(uuid.uuid4())
    database.add_instance_no_commit(Reservations,
                                    id=reservation_id,
                                    customer=body['idUser'],
                                    room='1')
    database.add_instance_no_commit(WeightRoomReservations,
                                    reservation_number=999,
                                    # FIXME TODO: MANDARGLI DA FRONT END/ fare query qui x prendersi il progressivo della reservation x quel determinato slot oppure eliminare il campo perche non viene mai usato
                                    reservation_id=reservation_id,
                                    slot=(body['idSlot']))
    database.commit_changes()
