import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from claimguard import ClaimGuard, Policy  # noqa: E402


def main() -> None:
    here = Path(__file__).resolve().parent
    policy = Policy.load(here / "policy.yaml")
    sample = json.loads((here / "sample_input.json").read_text(encoding="utf-8"))

    result = ClaimGuard(policy).verify(**sample)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

