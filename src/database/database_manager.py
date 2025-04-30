import sqlite3
from threading import Lock
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='cycle_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.lock = Lock()
        self._init_db()

    def _init_db(self):
        with self.lock:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS cycles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_date TEXT UNIQUE,
                    cycle_length INTEGER,
                    notes TEXT
                )''')
            self.conn.commit()

    def add_period(self, start_date, notes=''):
        with self.lock:
            # Calcular duración automáticamente
            last_entry = self.conn.execute(
                "SELECT start_date FROM cycles ORDER BY id DESC LIMIT 1"
            ).fetchone()
            
            if last_entry:
                last_date = datetime.strptime(last_entry[0], '%Y-%m-%d')
                cycle_length = (datetime.strptime(start_date, '%Y-%m-%d') - last_date).days
            else:
                cycle_length = 0
                
            self.conn.execute(
                "INSERT INTO cycles (start_date, cycle_length, notes) VALUES (?, ?, ?)",
                (start_date, cycle_length, notes)
            )
            self.conn.commit()