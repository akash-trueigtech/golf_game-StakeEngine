from dataclasses import dataclass, field
from typing import List




class Book:
    def __init__(self):
        self.events = []


    def add_event(self, event: dict):
        # ensure index correctness
        event["index"] = len(self.events)
        self.events.append(event)


@dataclass
class GameState:
    bet_amount: float = 1.0
    running_total_win: int = 0
    book: Book = field(default_factory=Book)


    @property
    def bet_amount_cents(self):
        return int(self.bet_amount * 100)