from dataclasses import dataclass, field


@dataclass
class Player:
    name: str
    lives: int = 3
    words_used: set = field(default_factory=set)

    def lose_life(self):
        self.lives -= 1

    def has_lives(self):
        return self.lives > 0
