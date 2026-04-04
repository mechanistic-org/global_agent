import os
import json
import datetime
import hashlib
from pathlib import Path
import logging

logger = logging.getLogger("NanoClaw")

# Pricing per 1M tokens (as of 2026 guidelines)
MODEL_PRICING_PER_1M = {
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-3.1-pro": {"input": 1.25, "output": 5.00},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
}

class TokenLedger:
    def __init__(self, ledger_path: str = None):
        if ledger_path is None:
            self.ledger_path = Path(__file__).parent.parent / ".system_generated" / "logs" / "token_ledger.json"
        else:
            self.ledger_path = Path(ledger_path)
            
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_ledger_exists()

    def _ensure_ledger_exists(self):
        if not self.ledger_path.exists():
            with open(self.ledger_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_ledger(self) -> dict:
        try:
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to load ledger: {e}")
            return {}

    def _save_ledger(self, data: dict):
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def record_usage(self, model_name: str, prompt_tokens: int, completion_tokens: int):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        ledger = self._load_ledger()
        
        if today not in ledger:
            ledger[today] = {}
        
        if model_name not in ledger[today]:
            ledger[today][model_name] = {"prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0.0}
            
        # Update tokens
        ledger[today][model_name]["prompt_tokens"] += prompt_tokens
        ledger[today][model_name]["completion_tokens"] += completion_tokens
        
        # Calculate cost
        pricing = MODEL_PRICING_PER_1M.get(model_name, MODEL_PRICING_PER_1M["gemini-2.5-flash"])
        p_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        c_cost = (completion_tokens / 1_000_000) * pricing["output"]
        
        ledger[today][model_name]["cost_usd"] += (p_cost + c_cost)
        
        self._save_ledger(ledger)
        total_cost = sum(m["cost_usd"] for m in ledger[today].values())
        logger.info(f"🪙 Ledger Updated: {model_name} | Daily Total: ${total_cost:.4f}")

    def get_daily_cost(self) -> float:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        ledger = self._load_ledger()
        if today not in ledger:
            return 0.0
        return sum(m["cost_usd"] for m in ledger[today].values())


class LoopDetector:
    def __init__(self, max_consecutive_identical: int = 3):
        self.max_identical = max_consecutive_identical
        self.history = []
        
    def _hash_content(self, text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def check_for_loop(self, content: str) -> bool:
        """Returns True if a loop is detected."""
        content_hash = self._hash_content(content)
        self.history.append(content_hash)
        
        if len(self.history) >= self.max_identical:
            recent = self.history[-self.max_identical:]
            if all(h == recent[0] for h in recent):
                return True
        return False
