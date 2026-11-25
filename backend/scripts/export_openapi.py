import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402

if __name__ == "__main__":
    output = Path(__file__).resolve().parents[1] / "openapi.json"
    output.write_text(json.dumps(app.openapi(), indent=2))
    print(f"Wrote {output}")
