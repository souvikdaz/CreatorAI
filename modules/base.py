import json
from pathlib import Path
from datetime import datetime, timezone
from core.config import Config
from core.db import Database
from core.quota import QuotaManager

class BaseModule:
    name: str = "base_module"

    def __init__(self, config: Config, db: Database, quota: QuotaManager):
        self.config = config
        self.db = db
        self.quota = quota

    def run(self, **kwargs) -> dict:
        raise NotImplementedError("Subclasses must implement run()")

    def to_markdown(self, result: dict) -> str:
        raise NotImplementedError("Subclasses must implement to_markdown()")

    def execute_and_export(self, output_dir: str = "output", **kwargs) -> tuple:
        """Runs the module, stores report in SQLite cache, and writes JSON & MD files."""
        result = self.run(**kwargs)
        md_text = self.to_markdown(result)

        # Save to SQLite reports cache
        self.db.save_report(self.name, result, md_text)

        # Export to files
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        json_file = out_path / f"{self.name}.json"
        md_file = out_path / f"{self.name}.md"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_text)

        return result, md_text

    @staticmethod
    def get_confidence(sample_count: int, has_private_analytics: bool = False) -> str:
        """Determines confidence level based on sample size and data fidelity."""
        if has_private_analytics and sample_count >= 10:
            return "HIGH"
        if sample_count >= 15:
            return "HIGH"
        if sample_count >= 5:
            return "MEDIUM"
        return "LOW"
