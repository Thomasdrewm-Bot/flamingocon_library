import sqlite3

class Database:
    def __init__(self, db_path="flamingocon_lib"):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def get_connection(self):
        return self.connection
    
    def close(self):
        self.connection.close()

    