from ..models import Users
from .. import app, database
from datetime import datetime
from ..response import Response, DATE_FORMAT, DATE_FORMAT_IN, TIME_FORMAT


def parse_slots():
    db_slots = database.get_all_slots_curent_reservation()
    slots = []
    for slot in db_slots:
        slots.append({
            "id": slot['id'],
            "date": (slot['date']).strftime(DATE_FORMAT),
            "time_from": slot['time_from'].strftime(TIME_FORMAT),
            "time_to": slot['time_to'].strftime(TIME_FORMAT),
            "max_capacity": slot['max_capacity'],
            "current_reservations": slot['current_reservations'],
            "title": slot['title'],
            "description": slot['description']
        })
    return slots
