import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


DEBUG_LOG_PATH = Path(__file__).resolve().parents[2] / "debug-bd2b9f.log"


def agent_debug_log(
    run_id: str,
    hypothesis_id: str,
    location: str,
    message: str,
    data: Dict[str, Any],
) -> None:
    payload = {
        "sessionId": "bd2b9f",
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(datetime.utcnow().timestamp() * 1000),
    }
    try:
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass

