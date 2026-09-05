from pathlib import Path


def test_patent_files_present():
    root = Path('output/meta_evolution_pkg_v2/docs')
    assert (root / 'claims_ru.txt').exists()
    assert (root / 'claims_en.txt').exists()
    assert (root / 'description_ru.txt').exists()
    assert (root / 'description_en.txt').exists()
