
class GameModel:
    def __init__(self,db):
        self.db = db

    # Create the table if it doesn't exist yet.
    def create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS games(
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(100) NOT NULL
                        )                        
                        """)

    # Add a game in    
    def add_game(self, name):
        sql_query = """
                INSERT INTO games (name)
                VALUEs (?)
                """
        with self.db.transaction():
            self.db.execute(sql_query, (name,))
    
    # Add a Bulk CSV of games in
    def bulk_add(self, games):
        with self.db.trasnaction():
            self.db.executemany(
                """
                INSERT INTO games (name)
                VALUES (?)
                """,
                games
            )
