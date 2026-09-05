# Meta Evolution

Semantic meta-evolution package with CLI, disk-backed memory, logging, config loading, and report generation.

## Install
```bash
pip install -e .
```

## Configuration
Copy `config.example.yaml` or `config.example.json` and edit values.

Example YAML:
```yaml
data_dir: output/meta_evolution_data
log_dir: output/meta_evolution_logs
interval_min: 0.5
interval_max: 1.0
report_every_seconds: 1800
acceptance_threshold: 0.7
```

Example JSON:
```json
{
  "data_dir": "output/meta_evolution_data",
  "log_dir": "output/meta_evolution_logs",
  "interval_min": 0.5,
  "interval_max": 1.0,
  "report_every_seconds": 1800,
  "acceptance_threshold": 0.7
}
```

## Run
```bash
meta-evolution run --input "опыт правило проблема символ" --kind text
```

## Outputs
- Persistent memory: `output/meta_evolution_data/memory.json`
- Registry: `output/meta_evolution_data/registry.json`
- Reports: `output/meta_evolution_data/reports.json`
- Logs: `output/meta_evolution_logs/meta_evolution.log`

## Tests
```bash
pytest
```
