
class GameRepos:
    def __init__(self,db):
        self.db = db

    # Create the table if it doesn't exist yet.
    def create_table(self):
        with self.db.transaction():
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS games (
                            game_id INTEGER PRIMARY KEY,
                            title VARCHAR(100) NOT NULL,
                            status ENUM('Available', 'Checked Out') NOT NULL,
                            barcode VARCHAR(255)
                            );                        
                            """)

    # Add a game in    
    def add(self, name):
        sql_query = """
                INSERT INTO games (name)
                VALUEs (?);
                """
        with self.db.transaction():
            self.db.execute(sql_query, (name,))
    
    # Add a Bulk CSV of games in
    def bulk_add(self, games):
        sql_query = """
                INSERT INTO games (name)
                VALUES (?);
                """
        with self.db.trasnaction():
            self.db.executemany(sql_query, games)

    # Update Game Info
    def update(self,game):
        sql_query = """
                UPDATE games
                SET name = ?
                WHERE id = ?;
                """
        with self.db.transaction():
            self.db.execute(sql_query, game)

    # Search for games tool
    def get_games(self, name):
        sql_query = """
                SELECT *
                WHERE name
                LIKE ?;
                """
        name = f"%{name}%"
        return self.db.fetchall(sql_query, (name,))
