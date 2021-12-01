import json

class Response:
    status = 200
    data = None
    message = None

    def toJSON(self):
        return {
            "status": self.status,
            "message": self.message,
            "data":(self.data) #default=lambda o: o.__dict__,sort_keys=True, indent=4)
        }