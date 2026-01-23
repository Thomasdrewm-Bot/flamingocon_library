class Game():
    def __init__(self,
                 game_id: int,
                 title: str,
                 status: str,
                 barcode: str
                 ):
        self.game_id = game_id
        self.title = title
        self.status = status
        self.barcode = barcode
        