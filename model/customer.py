from dataclasses import dataclass, field


@dataclass
class Customer():
    CustomerId: int
    FirstName: str
    LastName:str
    Phone: str
    Email: str

    artists: list = field(default_factory=list)
    genres: list = field(default_factory=list)

    def __hash__(self):
        return hash(self.CustomerId)

    def __eq__(self, other):
        return self.CustomerId == other.CustomerId

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"