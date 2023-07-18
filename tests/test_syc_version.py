import pytest

from ansys.systemcoupling.core.syc_version import normalize_version


def test_normalize_version_variations() -> None:
    assert normalize_version("231") == (23, 1)
    assert normalize_version("23.2") == (23, 2)
    assert normalize_version("22_1") == (22, 1)


def test_normalize_version_invalid() -> None:
    with pytest.raises(ValueError):
        normalize_version("")
    with pytest.raises(ValueError):
        normalize_version("22")
    with pytest.raises(ValueError):
        normalize_version("2212")
    with pytest.raises(ValueError):
        normalize_version("23.1.1")
    with pytest.raises(ValueError):
        normalize_version("231.2")
    with pytest.raises(ValueError):
        normalize_version("23a")
    with pytest.raises(ValueError):
        normalize_version("ab.2")
    with pytest.raises(ValueError):
        normalize_version("2.3.1")
    with pytest.raises(ValueError):
        normalize_version("2.3_2")
    with pytest.raises(ValueError):
        normalize_version("2_3.2")
