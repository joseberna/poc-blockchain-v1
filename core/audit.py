import logging
import sys

class AuditSystem:
    """Forensic Log Orchestrator."""
    def __init__(self):
        self._logger = logging.getLogger("ForensicNode")
        self._logger.setLevel(logging.INFO)
        # Clear existing handlers to prevent duplication
        self._logger.handlers = []
        
        # Format
        fmt = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s')
        
        # Terminal Stream
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        self._logger.addHandler(sh)
        
        # File Stream
        fh = logging.FileHandler("blockchain_audit.log")
        fh.setFormatter(fmt)
        self._logger.addHandler(fh)

    def log(self, msg: str, level: str = "info"):
        getattr(self._logger, level)(msg)

# Global Instance
audit = AuditSystem()
        
def log_event(msg: str, level: str = "info"):
    audit.log(msg, level)
