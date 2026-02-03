import sqlite3


class HotelModel:
    def __init__(self, db_path='hotel.db'):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    roomId INTEGER PRIMARY KEY AUTOINCREMENT,
                    floor INTEGER NOT NULL,
                    guestNum INTEGER NOT NULL,
                    beds INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    is_booked INTEGER DEFAULT 0
                )
            ''')
            # ПРОВЕРКА: Если база пустая, добавим пару комнат для тестов
            cursor = conn.execute("SELECT COUNT(*) FROM rooms")
            if cursor.fetchone()[0] == 0:
                conn.execute("INSERT INTO rooms (floor, guestNum, beds, price) VALUES (2, 1, 1, 2000)")
                conn.execute("INSERT INTO rooms (floor, guestNum, beds, price) VALUES (1, 2, 1, 2500)")
            conn.commit()

    def get_all_available(self):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM rooms WHERE is_booked = 0")
            return [dict(row) for row in cursor.fetchall()]

    def add_new_room(self, data):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO rooms (floor, guestNum, beds, price) VALUES (?, ?, ?, ?)",
                (data['floor'], data['guestNum'], data['beds'], data['price'])
            )
            conn.commit()

    def book_room_by_id(self, room_id):
        with self._get_connection() as conn:
            room = conn.execute("SELECT is_booked FROM rooms WHERE roomId = ?", (room_id,)).fetchone()
            if not room: return "NOT_FOUND"
            if room['is_booked'] == 1: return "ALREADY_BOOKED"

            conn.execute("UPDATE rooms SET is_booked = 1 WHERE roomId = ?", (room_id,))
            conn.commit()
            return "SUCCESS"