from dataclasses import dataclass


@dataclass
class Game():
     game_id: int
     title: str
     status: str
     barcode: str

     @property
     def id(self) -> int:
          return self.game_id
     
     @property
     def title(self) -> str:
          return self.title
     
     @property
     def status(self) -> str:
          return self.status
     
     @property
     def barcode(self) -> str:
          return self.barcode
     