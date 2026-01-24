class TransactionRepos:
    def __init__(self,db):
        self.db = db

    # Create the table if it doesn't exist yet.
    def create_table(self):
        with self.db.transaction():
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                            transaction_id INTEGER PRIMARY KEY,
                            checkout_game INT NOT NULL,
                            checkout_guest INT NOT NULL,
                            checkout_staff INT NOT NULL,
                            checkout_event INT NOT NULL,
                            time_checked_out TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                            CONSTRAINT fk_checkout_game
                                FOREIGN KEY (checkout_game)
                                REFERENCES games(game_id),

                            CONSTRAINT fk_checkout_guest
                                FOREIGN KEY (checkout_guest)
                                REFERENCES users(user_id),

                            CONSTRAINT fk_checkout_staff
                                FOREIGN KEY (checkout_staff)
                                REFERENCES users(user_id),

                            CONSTRAINT fk_checkout_event
                                FOREIGN KEY (checkout_event)
                                REFERENCES events(event_id)
                            );
                            """)
        
        # Create Transaction
        def transaction(self, params):
            sql_query = """
                    INSERT INTO transactions (checkout_game, checkout_guest, checkout_staff, checkout_event)
                    VALUES (?, ?, ?, ?);
                    """
            with self.db.transaction():
                self.db.execute(sql_query, params)


        # Search Transactions
        def search(self, game_id = None, guest_id = None, staff_id = None, event_id = None):
            # Start building statement
            sql_query = "SELECT * FROM transactions WHERE 1=1"
            params = []

            # Add filters Dynamically
            if game_id is not None:
                sql_query += " AND checkout_game = ?"
                params.append(game_id)

            if guest_id is not None:
                sql_query += " AND checkout_guest = ?"
                params.append(guest_id)

            if staff_id is not None:
                sql_query += " AND checkout_staff = ?"
                params.append(staff_id)

            if event_id is not None:
                sql_query += " AND checkout_event = ?"
                params.append(event_id)

            # Convert list into tuple to pass to query.
            params_tuple = tuple(params)

            results = self.db.fetchall(sql_query, params_tuple)

            return results