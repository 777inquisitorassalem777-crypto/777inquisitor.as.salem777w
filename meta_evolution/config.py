from dataclasses import dataclass
from pathlib import Path
import json

try:
    import yaml
except Exception:
    yaml = None

@dataclass
class Config:
    data_dir: Path = Path("output/meta_evolution_data")
    log_dir: Path = Path("output/meta_evolution_logs")
    interval_min: float = 0.5
    interval_max: float = 1.0
    report_every_seconds: int = 1800
    acceptance_threshold: float = 0.7

    @classmethod
    def default(cls):
        cfg = cls()
        cfg.data_dir.mkdir(parents=True, exist_ok=True)
        cfg.log_dir.mkdir(parents=True, exist_ok=True)
        return cfg

    @classmethod
    def from_file(cls, path):
        path = Path(path)
        if path.suffix.lower() in {'.yaml', '.yml'}:
            if yaml is None:
                raise RuntimeError('PyYAML is required for YAML config files')
            data = yaml.safe_load(path.read_text(encoding='utf-8'))
        else:
            data = json.loads(path.read_text(encoding='utf-8'))
        cfg = cls(**data)
        cfg.data_dir = Path(cfg.data_dir)
        cfg.log_dir = Path(cfg.log_dir)
        cfg.data_dir.mkdir(parents=True, exist_ok=True)
        cfg.log_dir.mkdir(parents=True, exist_ok=True)
        return cfg
