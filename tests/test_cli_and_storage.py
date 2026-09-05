import json
from meta_evolution.config import Config
from meta_evolution.core import MetaEvolutionCore, InputItem


def test_persistent_files_created():
    cfg = Config.default()
    core = MetaEvolutionCore(cfg)
    core.cycle(InputItem(kind='text', payload='опыт правило проблема', meta={'intent': 'persist'}))
    assert (cfg.data_dir / 'memory.json').exists()
    assert (cfg.data_dir / 'registry.json').exists()
    assert (cfg.data_dir / 'reports.json').exists()


def test_reload_state():
    cfg = Config.default()
    core1 = MetaEvolutionCore(cfg)
    core1.cycle(InputItem(kind='text', payload='символ паттерн алгоритм', meta={'intent': 'reload'}))
    core2 = MetaEvolutionCore(cfg)
    assert len(core2.memory) >= 1
    assert len(core2.registry) >= 1
