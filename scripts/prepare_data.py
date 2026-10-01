from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ML_SERVICE_ROOT = PROJECT_ROOT / "ml-service"
sys.path.insert(0, str(ML_SERVICE_ROOT))

from zeroguard_ml.preprocessing import main


if __name__ == "__main__":
    main()

