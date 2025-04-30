import sqlite3
from datetime import datetime
from threading import Lock

class DatabaseManager:
    def __init__(self, db_name='cycle_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.lock = Lock()
        self._initialize_db()

    def _initialize_db(self):
        with self.lock:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS cycles (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                start_date TEXT UNIQUE,
                                cycle_length INTEGER)''')
            self.conn.commit()

    def add_period(self, start_date):
        with self.lock:
            try:
                date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                prev_entry = self.conn.execute(
                    "SELECT start_date FROM cycles ORDER BY id DESC LIMIT 1"
                ).fetchone()
                
                if prev_entry:
                    prev_date = datetime.strptime(prev_entry[0], '%Y-%m-%d')
                    cycle_length = (date_obj - prev_date).days
                    self.conn.execute(
                        "INSERT INTO cycles (start_date, cycle_length) VALUES (?, ?)",
                        (start_date, cycle_length)
                    )
                else:
                    self.conn.execute(
                        "INSERT INTO cycles (start_date) VALUES (?)",
                        (start_date,)
                    )
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Database error: {e}")
                return False

    def get_all_periods(self):
        with self.lock:
            return self.conn.execute(
                "SELECT start_date, cycle_length FROM cycles ORDER BY start_date DESC"
            ).fetchall()

    def get_cycle_stats(self):
        with self.lock:
            data = self.conn.execute(
                "SELECT cycle_length FROM cycles WHERE cycle_length IS NOT NULL"
            ).fetchall()
            return [x[0] for x in data] if data else []