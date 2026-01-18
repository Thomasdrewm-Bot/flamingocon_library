import bcrypt

class UserModel:
    def __init__(self,db):
        self.db = db.get_connection()
        self.cursor = self.db.cursor()

    # Create the table if it doesn't exist yet.
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        first_name VARCHAR(35) NOT NULL,
                        last_name VARCHAR(35) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        role VARCHAR(20) DEFAULT 'Guest',
                        password VARCHAR(255),
                        LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )                        

                        """)
     # add users to the table   
    def add_user(self, new_user):
        sql_query = """
            INSERT INTO users (first_name, last_name, email)
            VALUES (?, ?, ?)
            """
        self.cursor.execute(sql_query, new_user)
        self.db.commit()

    # Get users from the table, defaults to sending back all users.
    def get_users(self, user = "All"):

        if user == "All":
            sql_query = """
                SELECT * 
                FROM users
                """
            self.cursor.execute(sql_query)
        else:
            sql_query = """
                SELECT *
                FROM users
                WHERE first_name LIKE ?
                AND last_name LIKE ?
                """
            self.cursor.execute(sql_query, user)
        
        return self.cursor.fetchall()
    
    # Grab a specific user's records
    def get_user(self, user_id):
        sql_query = """
                SELECT *
                FROM users
                WHERE id = ?
                """
        self.cursor.execute(sql_query, user_id)
        return self.cursor.fetchone()
            
    # Delete a user from the table.
    def del_user(self, user_id):
        sql_query = """
                DELETE FROM users
                WHERE id is ?
                """
        self.cursor.execute(sql_query, user_id)
        self.db.commit()

    # Update user information
    def update_user(self, record):
        pass


    # Promote a user role in the table
    def promote_user(self, user, new_role):
        sql_query ="""
                UPDATE users
                SET role = ?,
                WHERE id = ?"""
        self.cursor.execute(sql_query, (new_role, user))
        self.db.commit()

    # Set user password when given a role that can log in.
    def set_pw(self, user_id, pw):
        # Convert the password into bytes, necessary for bcrypt
        bytes_pw = pw.encode('utf-8')
        # Hash the password with bcrypt
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        sql_query = """
                UPDATE users
                SET password = ?,
                WHERE id = ?
                """
        self.cursor.execute(sql_query, (hashed_pw, user_id))
        self.db.commit()

    # Verify the user password, return true or false
    def verify_pw(self, user_id, entered_pw):
        # grabs the stored password
        self.cursor.execute("SELECT password FROM users WHERE id = ?", user_id)
        user_stored_pw = self.cursor.fetchone()
        # Converts and checks the password entered against the stored password
        result = bcrypt.checkpw(entered_pw.encode('utf-8'), user_stored_pw)
        return result