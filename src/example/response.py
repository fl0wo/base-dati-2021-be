import json


class Response:
    def __init__(self):
        pass

    status = 200
    data = None
    message = None

    def toJSON(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data  # default=lambda o: o.__dict__,sort_keys=True, indent=4)
        }


DATE_FORMAT = '%Y/%m/%d'
DATE_FORMAT_IN = '%Y-%m-%d'
TIME_FORMAT = "%H:%M:%S"
