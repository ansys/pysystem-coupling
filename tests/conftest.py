import pytest

pytest_plugins = []


@pytest.fixture
def with_launching_container(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SYC_LAUNCH_CONTAINER", "1")
