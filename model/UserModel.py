

class UserModel:
    def __init__(self,db):
        self.db = db.get_connection()

    def create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        role TEXT DEFAULT 'Guest',
                        passwd TEXT,
                        LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )                        

                        """)
        
    def add_user(self, new_user):
        sql_query = """
            INSERT INTO users (first_name, last_name, email)
            VALUES (?, ?, ?)
            """
        self.db.execute(sql_query, new_user)
        self.db.commit()

    def get_users(self, user = "All"):

        if user == "All":
            sql_query = """
                SELECT * from users
                """
            cursor = self.db.execute(sql_query)
        else:
            sql_query = """
                SELECT *
                FROM users
                WHERE first_name LIKE ?
                AND last_name LIKE ?
                """
            cursor = self.db.execute(sql_query, user)
        
        return cursor.fetchall()
            
    
    def del_user(self, user):
        sql_query = """
                DELETE FROM users
                WHERE id is ?
                """
        self.db.execute(sql_query, user)
        self.db.commit()

    def promote_user(self, user, new_role):
        sql_query ="""
                UPDATE users
                SET role = ?,
                WHERE id = ?"""
        self.db.execute(sql_query, (new_role, user))
        self.db.commit()
