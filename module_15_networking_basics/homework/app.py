from flask import Flask, request, jsonify
from service import HotelService

app = Flask(__name__)
service = HotelService()


# Уровень 2: Используем существительное 'rooms'
@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = service.get_rooms_list()
    return jsonify({"rooms": rooms}), 200


# Уровень 2: POST на коллекцию ресурсов для создания
@app.route('/rooms', methods=['POST'])
def add_room():
    data = request.get_json(force=True)
    updated_rooms = service.add_room(data)
    # Возвращаем 201 Created согласно модели Ричардсона
    return jsonify({"rooms": updated_rooms}), 201


# Уровень 2: PATCH для изменения состояния конкретного ресурса по ID
@app.route('/rooms/<int:room_id>', methods=['PATCH'])
def book_room(room_id):
    # Тело запроса может быть пустым или содержать статус,
    # но сам ID мы берем из URL
    result = service.book_room(room_id)

    if result == "SUCCESS":
        return jsonify({"message": f"Room {room_id} booked"}), 200
    elif result == "ALREADY_BOOKED":
        return "Conflict: Room already booked", 409
    else:
        return jsonify({"error": "Room not found"}), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)