import datetime
import json
import hashlib
from typing import Any, Dict, List

class Block:
    """The Encapsulated Cryptographic Block."""
    def __init__(self, index: int, proof: int, previous_hash: str, transactions: List[Dict[str, Any]]):
        self.index = index
        self.proof = proof
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return vars(self)

    @staticmethod
    def calculate_hash(block_dict: Dict[str, Any]) -> str:
        """Generates a SHA-256 fingerprint for a block's core data."""
        # Immutable check: exclude status/dynamic fields if any
        payload = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()
