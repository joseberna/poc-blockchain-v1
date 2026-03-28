import datetime
from typing import Any, Dict

class Transaction:
    """Atomic Unit of Asset Transfer."""
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = float(amount)
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return vars(self)
