import bcrypt
from model.User import User

class UserRepos:
    def __init__(self,db):
        self.db = db

    # Create the table if it doesn't exist yet.
    def create_table(self):
        with self.db.transaction():
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            first_name VARCHAR(50) NOT NULL,
                            last_name VARCHAR(50) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            role NOT NULL DEFAULT 'Guest'
                            check (role in ('Guest', 'Volunteer', 'Staff', 'Staff-Admin')),
                            password BLOB,
                            username VARCHAR(50),
                            LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );                        
                            """)

     # Create
    def add(self, first_name, last_name, email):
        sql_query = """
            INSERT INTO users (first_name, last_name, email)
            VALUES (?, ?, ?);
            """
        with self.db.transaction():
            self.db.execute(sql_query, (first_name, last_name, email,))

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

    # Read
    # Get all users
    def get_all_users(self):
        return self.db.fetchall("SELECT * FROM users;")
        
    # Search for users by name
    def search_by_name(self, fname, lname):
            fname = f"%{fname}%"
            lname = f"%{lname}%"
            sql_query = """
                SELECT *
                FROM users
                WHERE first_name LIKE ?
                AND last_name LIKE ?;
                """
            return self.db.fetchall(sql_query, (fname,lname,))
    
    # Grab a specific user's records
    def get_by_user_id(self, user_id):
        return self.db.fetchone("SELECT * FROM users WHERE user_id = ?;", (user_id,))
    
    # Get login users
    def get_log_in_users(self):
        user_list = self.deb.fetchall("SELECT * FROM users WHERE role <> ? ORDER BY name ASC;", ('Guest',))
        for users in user_list:

            



    # Delete
    def delete_user(self, user_id):
        with self.db.transaction():
            self.db.execute("DELETE FROM users WHERE user_id = ?;", (user_id,))



    # Update user information
    def update(self, f_name, l_name, email, user_id):
        sql_query = """
                UPDATE users
                SET first_name = ?,
                last_name = ?,
                email = ?
                WHERE user_id = ?;
                """
        with self.db.transaction():
            self.db.execute(sql_query, (f_name, l_name, email, user_id,))



    # Promote a user role in the table
    def promote_user(self, user_id, new_role, username):
        sql_query ="""
                UPDATE users
                SET role = ?
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
                SET password = ?
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
    
    def row_to_user(self, row) -> User | None:
        if not row:
            return None
        
        return User(
            user_id = row[0],
            first_name = row[1],
            last_name = row[2],
            email = row[3],
            role = row[4],
            username = row[6]
        )