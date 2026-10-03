import json
from pathlib import Path

class UserEvolution:
    def __init__(self, user_id="default_user"):
        self.path = Path("memory") / f"{user_id}.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._save({
                "user_id": user_id,
                "capabilities": [],
                "evolution_proposals": []
            })

    def _load(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, data):
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_profile(self):
        return self._load()

    def add_proposal(self, proposal):
        data = self._load()
        data["evolution_proposals"].append(proposal)
        self._save(data)
