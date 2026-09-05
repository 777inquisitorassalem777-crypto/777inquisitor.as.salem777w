from meta_evolution.config import Config


def test_default_config_paths():
    cfg = Config.default()
    assert cfg.data_dir.exists()
    assert cfg.log_dir.exists()
