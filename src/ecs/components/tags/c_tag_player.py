

class CTagPlayer:
    def __init__(self, lives: int) -> None:
        self.active = True
        self.lives = lives
        self.left = False
        self.right = False

