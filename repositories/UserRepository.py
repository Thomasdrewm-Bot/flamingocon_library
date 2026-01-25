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
                                check (role in ('Guest','Volunteer','Staff','Staff-Admin')),
                            password BLOB,
                            can_login INTEGER NOT NULL DEFAULT 0
                                CHECK (can_login IN (0,1)),
                            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );                        
                            """)

     # ---------------Create---------------
    def add(self, first_name, last_name, email):
        with self.db.transaction():
            self.db.execute(
                """
                INSERT INTO users (first_name, last_name, email)
                VALUES (?, ?, ?);
                """,
                (first_name, last_name, email)
            )

    # Bulk add users
    def bulk_add(self, users):
        with self.db.transaction():
            self.db.executemany("""
                    INSERT INTO users (first_name, last_name, email)
                    VALUES (?, ?, ?);
                """,
                users
            )

    # ---------------Read---------------

    # Get all users
    def get_all_users(self) -> list[User]:
        rows = self.db.fetchall("""
                SELECT user_id, first_name, last_name, email, role
                FROM users
                ORDER BY last_name, first_name;
            """
        )
        return [User.from_row(row) for row in rows]
        
    # Search for users by name
    def search_by_name(self, fname, lname) -> list[User]:
            rows = self.db.fetchall("""
                    SELECT user_id, first_name, last_name, email, role
                    FROM users
                    WHERE first_name LIKE ?
                    AND last_name LIKE ?;
                """,
                (f"%{first_name}%", f"%{last_name}%")
            )
            return [User.from_row(row) for row in rows]
    
    # Get login users
    def get_login_users(self) -> list[User]:
        rows = self.db.fetchall("""
                SELECT
                    user_id,
                    first_name,
                    last_name,
                    email,
                    role
                FROM users
                WHERE can_login = 1
                ORDER BY last_name, first_name;
            """)
        return [User.from_row(row) for row in rows]
    
    # Grab a specific user's records
    def get_by_user_id(self, user_id) -> User | None:
        row = self.db.fetchone("""
                SELECT user_id, first_name, last_name, email, role
                FROM users
                WHERE user_id = ?;
            """, (user_id,))
        return User.from_row(row) if row else None

    # ---------------Update---------------

    # Update user information
    def update(self, first_name, last_name, email, user_id):
        with self.db.transaction():
            self.db.execute("""
                    UPDATE users
                    SET first_name = ?,
                    last_name = ?,
                    email = ?
                    WHERE user_id = ?;
                """,
                (first_name, last_name, email, user_id)
            )



    # Promote a user role in the table
    def promote_user(self, user_id, new_role):
        with self.db.transaction():
            self.db.execute("""
                    UPDATE users
                    SET role = ?, can_login = 1
                    WHERE user_id = ?;
                """,
                (new_role, user_id)
            )

    # Set user password when given a role that can log in.
    def set_password(self, user_id, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with self.db.transaction():
            self.db.execute(
                "UPDATE users SET password = ? WHERE user_id = ?;",
                (hashed, user_id)
            )

    # Verify the user password, return true or false
    def verify_pw(self, user_id, entered_password) -> bool:

        # grabs the stored password
        row = self.db.fetchone(
            "SELECT password FROM users WHERE user_id = ?;", 
            (user_id,)
            )
        
        # Checks if a valid record was even returned first
        if not row or not row["password"]:
            return False

        # Converts and checks the password entered against the stored password
        return bcrypt.checkpw(
            entered_password.encode('utf-8'),
            row["password"]
        )
    
    # ---------------Delete---------------
    
    def delete_user(self, user_id):
        with self.db.transaction():
            self.db.execute(
                "DELETE FROM users WHERE user_id = ?;",
                (user_id,)
            )