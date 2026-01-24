class EventRepos:
    def __init__(self,db):
        self.db = db

    # Create the table if it doesn't exist yet.
    def create_table(self):
        with self.db.transaction():
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS events (
                            event_id INTEGER PRIMARY KEY,
                            name VARCHAR(50) NOT NULL,
                            first_day DATE NOT NULL,
                            end_day DATE NOT NULL,
                            location VARCHAR(255),
                            created_by_user_id INT NOT NULL,

                            CONSTRAINT fk_events_created_by
                                FOREIGN KEY (created_by_user_id)
                                REFERENCES users(user_id)
                            );""")
        
    # Add an event
    def add(self, event):
        sql_query = """
                INSERT INTO events (name, first_day, end_day, location)
                VALUES (?, ?, ?, ?)
                """
        with self.db.transaction():
            self.db.execute(sql_query, event)

    def get_events(self):
        return self.db.fetchall("SELECT * FROM events;")
    
    def get_event(self, event_id):
        return self.db.fetchone("SELECT * FROM events WHERE event_id = ?;", (event_id,))
    
