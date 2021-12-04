from ..response import Response, DATE_FORMAT, \
    DATE_FORMAT_IN, TIME_FORMAT

def format_date(date):
    if date is None:
        return None
    return date.strftime(DATE_FORMAT)