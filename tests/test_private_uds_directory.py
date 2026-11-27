# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
"""Tests for private local session directory provisioning."""

import os
from pathlib import Path
import stat

import pytest

from ansys.systemcoupling.core.client.private_uds_directory import PrivateUdsDirectory

pytestmark = pytest.mark.skipif(os.name == "nt", reason="POSIX directory semantics")


def test_private_directory_is_created_and_removed(tmp_path):
    base = tmp_path / "not-created-yet"
    directory = PrivateUdsDirectory(base)
    path = directory.path
    assert path.parent == base
    assert stat.S_IMODE(base.stat().st_mode) == 0o700
    assert stat.S_IMODE(path.stat().st_mode) == 0o700
    assert path.stat().st_uid == os.geteuid()
    directory.close()
    assert not path.exists()
    directory.close()


def test_existing_readable_base_is_preserved(tmp_path):
    base = tmp_path / ".conn"
    base.mkdir(mode=0o755)
    base.chmod(0o755)
    directory = PrivateUdsDirectory(base)
    path = directory.path
    assert stat.S_IMODE(base.stat().st_mode) == 0o755
    assert stat.S_IMODE(path.stat().st_mode) == 0o700
    directory.close()
    assert stat.S_IMODE(base.stat().st_mode) == 0o755


def test_cleanup_preserves_nonempty_directory(tmp_path):
    directory = PrivateUdsDirectory(str(tmp_path))
    path = directory.path
    (path / "other").write_text("preserve")
    with pytest.raises(OSError):
        directory.close()
    assert (path / "other").read_text() == "preserve"


def test_cleanup_does_not_remove_replacement(tmp_path):
    directory = PrivateUdsDirectory(str(tmp_path))
    path = directory.path
    moved = path.with_name("moved")
    path.rename(moved)
    path.mkdir()
    directory.close()
    assert path.is_dir()
    assert moved.is_dir()


def test_symlink_home_is_rejected(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    link = tmp_path / "link"
    link.symlink_to(home, target_is_directory=True)
    with pytest.raises(OSError):
        PrivateUdsDirectory(str(link))
    assert list(home.iterdir()) == []


def test_writable_home_is_rejected(tmp_path):
    home = tmp_path / "home"
    home.mkdir(mode=0o700)
    home.chmod(0o777)
    try:
        with pytest.raises(PermissionError):
            PrivateUdsDirectory(str(home))
        assert list(home.iterdir()) == []
    finally:
        home.chmod(0o700)


def test_untrusted_root_is_rejected():
    with pytest.raises(PermissionError):
        PrivateUdsDirectory(str(Path("/")))


def test_sticky_shared_directory_can_contain_private_session(tmp_path):
    directory = PrivateUdsDirectory("/tmp")
    path = directory.path
    assert path.parent == Path("/tmp")
    assert stat.S_IMODE(path.stat().st_mode) == 0o700
    directory.close()
    assert not path.exists()
