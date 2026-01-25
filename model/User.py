from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    email: str
    role: str

    @property
    def full_name(self)-> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def id(self)-> int:
        return self.user_id
    
    @property
    def email(self) -> str:
        return self.email
    
    @classmethod
    def from_row(cls, row) -> "User":
        return cls(
            user_id=row["user_id"],
            first_name = row["first_name"],
            last_name = row["last_name"],
            email = row["email"],
            role = row["role"],
        )