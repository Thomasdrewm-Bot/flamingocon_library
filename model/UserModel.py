import bcrypt

class UserModel:
    def __init__(self,db):
        self.db = db

    # Create the table if it doesn't exist yet.
    def create_table(self):
        with self.db.transaction():
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            first_name VARCHAR(35) NOT NULL,
                            last_name VARCHAR(35) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            role VARCHAR(20) DEFAULT 'Guest',
                            password VARCHAR(255),
                            LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );                        
                            """)

     # add users to the table   
    def add(self, new_user: tuple = ()):
        sql_query = """
            INSERT INTO users (first_name, last_name, email)
            VALUES (?, ?, ?);
            """
        with self.db.transaction():
            self.db.execute(sql_query, new_user)

    # Bulk add users
    def bulk_add(self, users):
        with self.db.transaction():
            self.db.executemany(
                """
                INSERT INTO users (first_name, last_name, email)
                VALUES (?, ?, ?);
                """,
                users
            )

    # Get users from the table, defaults to sending back all users.
    def get_users(self, user = "All"):

        if user == "All":
            sql_query = """
                SELECT * 
                FROM users;
                """
            return self.db.fetchall(sql_query)
        else:
            sql_query = """
                SELECT *
                FROM users
                WHERE first_name LIKE ?
                AND last_name LIKE ?;
                """
            return self.db.fetchall(sql_query, (user,))
    
    # Grab a specific user's records
    def get_user(self, user_id):
        sql_query = """
                SELECT *
                FROM users
                WHERE user_id = ?;
                """
        return self.db.fetchone(sql_query, (user_id,))
            
    # Delete a user from the table.
    def del_user(self, user_id):
        sql_query = """
                DELETE FROM users
                WHERE user_id is ?;
                """
        with self.db.transaction():
            self.db.execute(sql_query, (user_id,))

    # Update user information
    def update(self, record):
        sql_query = """"
                UPDATE users
                SET first_name = ?,
                last_name = ?,
                email = ?
                WHERE user_id = ?;
                """
        with self.db.transaction():
            self.db.execute(sql_query, record)

    # Promote a user role in the table
    def promote_user(self, user_id, new_role):
        sql_query ="""
                UPDATE users
                SET role = ?,
                WHERE user_id = ?;
                """
        with self.db.transaction():
            self.db.execute(sql_query, (new_role, user_id,))

    # Set user password when given a role that can log in.
    def set_pw(self, user_id, pw):
        # Convert the password into bytes, necessary for bcrypt
        bytes_pw = pw.encode('utf-8')
        # Hash the password with bcrypt
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        sql_query = """
                UPDATE users
                SET password = ?,
                WHERE user_id = ?;
                """
        with self.db.transaction():
            self.db.execute(sql_query, (hashed_pw, user_id,))

    # Verify the user password, return true or false
    def verify_pw(self, user_id, entered_pw):
        # grabs the stored password
        user_stored_pw = self.db.fetchone("SELECT password FROM users WHERE user_id = ?;", (user_id,))

        # Converts and checks the password entered against the stored password
        result = bcrypt.checkpw(entered_pw.encode('utf-8'), user_stored_pw)
        return result