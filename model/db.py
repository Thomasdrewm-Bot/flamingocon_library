import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_path="flamingocon_lib"):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    # Execute wrapper
    def execute(self, query: str, params: tuple = ()):
        return self.connection.execute(query, params)
    
    # Commit wrapper
    def commit(self):
        self.connection.commit()
    
    # close wrapper
    def close(self):
        self.connection.close()
    
    # Cursor like fetchone
    def fetchone(self, query: str, params: tuple = ()):
        cur = self.connection.execute(query,params)
        return cur.fetchone()
    
    # Cursor like fetchall
    def fetchall(self, query: str, params: tuple = ()):
        cur = self.connection.execute(query,params)
        return cur.fetchall()
    
    # Executemany Wrapper
    def executemany(self, query, params_list):
        return self.connection.executemany(query, params_list)
    
    @contextmanager
    def transaction(self):
        try:
            yield
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    