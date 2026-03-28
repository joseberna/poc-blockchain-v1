import hashlib
from typing import Any, Dict, List, Optional, Tuple
from core.block import Block
from core.transaction import Transaction

class BlockchainProtocol:
    """The Consensus Engine for the Forensic Ledger."""
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.mempool: List[Dict[str, Any]] = []
        self.difficulty: int = difficulty
        self._initialize_genesis()

    def _initialize_genesis(self) -> None:
        """Bootstraps the ledger with Node #1."""
        genesis_tx = [Transaction("System", "Satoshi", 0.0).to_dict()]
        self.create_block(proof=1, previous_hash='0', transactions=genesis_tx)

    def add_transaction(self, sender: str, receiver: str, amount: float) -> int:
        """Adds a new transaction to the mempool."""
        tx = Transaction(sender, receiver, amount).to_dict()
        self.mempool.append(tx)
        return self.get_last_block().index + 1

    def create_block(self, proof: int, previous_hash: str, transactions: Optional[List[Dict[str, Any]]] = None) -> Block:
        """Processes the commit of a new block into the main chain."""
        txs = transactions if transactions is not None else list(self.mempool)
        # Reset mempool only if we used it (not for Genesis)
        if transactions is None:
            self.mempool = []
            
        block = Block(
            index=len(self.chain) + 1,
            proof=proof,
            previous_hash=previous_hash,
            transactions=txs
        )
        self.chain.append(block)
        return block

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def solve_pow(self, prev_proof: int, override_diff: Optional[int] = None) -> int:
        """Executes the Proof-of-Work algorithm."""
        diff = override_diff if override_diff is not None else self.difficulty
        target = '0' * diff
        nonce = 1
        
        while True:
            # Deterministic PoW check
            fingerprint = hashlib.sha256(str(nonce**2 - prev_proof**2).encode()).hexdigest()
            if fingerprint.startswith(target):
                return nonce
            nonce += 1

    def validate_integrity(self) -> Tuple[bool, List[int]]:
        """Scans the ledger to detect forensic anomalies."""
        broken_indices = []
        if not self.chain:
            return True, []
            
        for i in range(1, len(self.chain)):
            prev = self.chain[i-1]
            curr = self.chain[i]
            
            # Check Hash Linkage
            if curr.previous_hash != Block.calculate_hash(prev.to_dict()):
                # Subsequent blocks are considered untrusted once the chain is broken
                broken_indices.extend(range(i, len(self.chain)))
                return False, sorted(list(set(broken_indices)))
        
        return True, []
