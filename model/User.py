class User:
    def __init__(
            self,
            user_id: int,
            first_name: str,
            last_name: str,
            email: str,
            role: str
            ):
        
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role


    @property
    def can_login(self):
        return self.role in ("Staff", "Staff-Admin", "Volunteer")
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def id(self):
        return self.user_id
        

