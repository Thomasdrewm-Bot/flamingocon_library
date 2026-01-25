from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    email: str
    role: str

    def can_login(self):
        return self.role in ("Staff", "Staff-Admin", "Volunteer")


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def id(self):
        return self.user_id
    
    @classmethod
    def from_row(cls, row):
        return cls(
            user_id=row["user_id"],
            first_name = row["first_name"],
            last_name = row["last_name"],
            email = row["email"],
            role = row["role"],
        )