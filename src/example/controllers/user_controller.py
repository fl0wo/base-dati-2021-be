from ..models import Users
from .. import app, database
from datetime import datetime
from ..response import Response, DATE_FORMAT, DATE_FORMAT_IN, TIME_FORMAT


def parse_me(user: Users):
    return {
        "name": user.name,
        "surname": user.surname,
        "role": user.role,
        "email": user.email,
        "birth_date": user.birth_date,
        "fiscal_code": user.fiscal_code,
        "phone": user.phone
    }

def update_me(user, request):
    body = request.get_json()
    birth_date = body['birth_date']
    if birth_date is not None:
        birth_date = datetime.strptime(body['birth_date'], DATE_FORMAT_IN).date()

    database.edit_instance(Users, id=user.id,
                           birth_date=birth_date,
                           fiscal_code=body['fiscal_code'],
                           phone=body['phone'])


def parse_my_res(user):
    my_reservations = database.get_reservations_of(user.id)
    subscription_data = []
    for sub in my_reservations:
        subscription_data.append({
            "reservation_type": sub.reservation_type,
            "date": sub.date.strftime(DATE_FORMAT),
            "time": sub.time.strftime(TIME_FORMAT),
            "participant_number": sub.participant_number,
            "slot": sub.slot
        })
    return subscription_data