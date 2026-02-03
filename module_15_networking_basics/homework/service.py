from models import HotelModel

class HotelService:
    def __init__(self):
        self.model = HotelModel()

    def get_rooms_list(self):
        return self.model.get_all_available()

    def add_room(self, data):
        self.model.add_new_room(data)
        # По требованиям тестов, после добавления возвращаем весь список
        return self.get_rooms_list()

    def book_room(self, room_id):
        return self.model.book_room_by_id(room_id)