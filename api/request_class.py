from .models import Booking

class Request:
    def __init__(self, request) -> None:
        self.request = request
        self.data = {}
        
    def add_user(self, user_id):
        for key in self.request.data:
            self.data[key] = self.request.data[key]
        self.data["user"] = user_id
        