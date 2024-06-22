import sqlite3
from datetime import timedelta, datetime

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
    
    def executemany(self, query, params):
        self.cursor.executemany(query, params)

    def fetchall(self):
        return self.cursor.fetchall()
    
class LegendsData:
    def __init__(self):
        self.db_name = 'database.db'

    def create_table(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS Legends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                description TEXT
            )
            ''')
    
    def insert_legend(self, color, description):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            INSERT INTO Legends (color, description)
            VALUES (?, ?)
            ''', (color, description))
    
    def insert_legends(self, legends):
        with DatabaseConnection(self.db_name) as db:
            db.executemany('''
            INSERT INTO Legends (color, description)
            VALUES (?, ?)
            ''', legends)
    
    def delete_legend(self, color):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            DELETE FROM Legends WHERE color == ?
            ''', (color,))


    def fetch_all_legends(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('SELECT color, description FROM Legends')
            rows = db.fetchall()
            legends_dict = {color: description for color, description in rows}
            return legends_dict
class EventData:
    def __init__(self):
        self.db_name = 'database.db'

    def create_table(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS Event (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL,
                headline TEXT,
                marks TEXT,
                text TEXT,
                date TEXT UNIQUE
            )
            ''')

    def insert_event(self, number, headline, marks, text, date):
        with DatabaseConnection(self.db_name) as db:
            try:
                db.execute('''
                INSERT INTO Event (number, headline, marks, text, date)
                VALUES (?, ?, ?, ?, ?)
                ''', (number, headline, marks, text, date))
            except sqlite3.IntegrityError:
                db.execute('''
                UPDATE Event
                SET number = ?, headline = ?, marks = ?, text = ?, date = ?
                WHERE date = ?
                ''', (number, headline, marks, text, date, date))

    def fetch_all_events(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('SELECT * FROM Event')
            return db.fetchall()

    def delete_event(self, event_id):
        with DatabaseConnection(self.db_name) as db:
            db.execute('DELETE FROM Event WHERE id = ?', (event_id,))


class NotesData:
    def __init__(self):
        self.db_name = 'database.db'

    def create_table(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('DROP TABLE IF EXISTS Notes')
            db.execute('DROP TABLE IF EXISTS HistoricalNotes')
            db.execute('''
            CREATE TABLE IF NOT EXISTS Notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                creation_date TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES Event (id)
            )
            ''')
            db.execute('''
            CREATE TABLE IF NOT EXISTS HistoricalNotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                creation_date TEXT NOT NULL,
                transfer_date TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES Event (id)
            )
            ''')



    def insert_note_with_event(self, event_id):
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with DatabaseConnection(self.db_name) as db:
            db.execute('''
            INSERT INTO Notes (event_id, creation_date)
            VALUES (?, ?)
            ''', (event_id, creation_date))

    def fetch_all_notes(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('SELECT * FROM Notes')
            return db.fetchall()

    def transfer_old_notes(self):
        cutoff_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        with DatabaseConnection(self.db_name) as db:
            # Select notes older than one day
            db.execute('''
            SELECT * FROM Notes WHERE creation_date <= ?
            ''', (cutoff_date,))
            old_notes = db.fetchall()

            # Insert old notes into HistoricalNotes
            for note in old_notes:
                event_id, creation_date = note[1], note[2]
                transfer_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.execute('''
                INSERT INTO HistoricalNotes (event_id, creation_date, transfer_date)
                VALUES (?, ?, ?)
                ''', (event_id, creation_date, transfer_date))

            # Delete old notes from Notes
            db.execute('''
            DELETE FROM Notes WHERE creation_date <= ?
            ''', (cutoff_date,))
    
    def fetch_all_historical_notes(self):
        with DatabaseConnection(self.db_name) as db:
            db.execute('SELECT * FROM HistoricalNotes')
            return db.fetchall()


legends_data = LegendsData()
legends_data.create_table()

event_data = EventData()
event_data.create_table()

notes_data = NotesData()
notes_data.create_table()

# Добавление примера данных
event_data.insert_event(1, "Sample Headline", "Sample Marks", "Sample Text", "2024-06-12")
notes_data.insert_note_with_event(1)
legends_data.insert_legend("Red", "This is a red legend")

# Перемещение старых заметок в историю
notes_data.transfer_old_notes()

# Получение данных
print(legends_data.fetch_all_legends())
print(event_data.fetch_all_events())
print(notes_data.fetch_all_notes())
print(notes_data.fetch_all_historical_notes())
