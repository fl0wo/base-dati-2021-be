from .. import app, database
from datetime import datetime
from ..response import Response, DATE_FORMAT, DATE_FORMAT_IN, TIME_FORMAT


def parse_lessons():
    db_lessons = database.get_all_lessons_curent_reservation()
    lessons = []
    for lesson in db_lessons:
        lessons.append({
            "id": lesson['id'],
            "date": (lesson['date']).strftime(DATE_FORMAT),
            "time": lesson['time'].strftime(TIME_FORMAT),
            "max_participants": lesson['max_participants'],
            "current_reservations": lesson['current_reservations'],
            "course": lesson['course'],
            "course_description": lesson['course_description']
        })
    return lessons
