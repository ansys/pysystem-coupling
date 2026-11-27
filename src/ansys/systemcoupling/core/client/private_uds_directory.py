# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
"""Private directory provisioning for locally launched POSIX UDS sessions."""

import os
from pathlib import Path
import stat
from uuid import uuid4


class PrivateUdsDirectory:
    """Own an empty, private session directory under a trusted UDS directory.

    The caller must stop the server before cleanup. Cleanup removes only the
    original empty directory; it never recursively deletes an endpoint or a
    replacement directory.
    """

    def __init__(self, base_directory: str | Path):
        if not all(
            hasattr(os, name) for name in ("O_DIRECTORY", "O_NOFOLLOW", "geteuid")
        ):
            raise OSError("Secure UDS directory operations are unavailable")
        if any(
            func not in os.supports_dir_fd
            for func in (os.open, os.mkdir, os.stat, os.rmdir)
        ):
            raise OSError("Secure UDS directory operations are unavailable")
        path = Path(os.path.abspath(base_directory))
        if path == Path("/"):
            raise PermissionError("UDS base directory must not be the filesystem root")
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        parent = os.open("/", flags)
        self._parent = None
        self._name = None
        try:
            for name in path.parts[1:]:
                self._check_ancestor(os.fstat(parent))
                try:
                    child = os.open(name, flags, dir_fd=parent)
                except FileNotFoundError:
                    try:
                        os.mkdir(name, 0o700, dir_fd=parent)
                    except FileExistsError:
                        pass
                    child = os.open(name, flags, dir_fd=parent)
                os.close(parent)
                parent = child
            info = os.fstat(parent)
            self._check_ancestor(info)

            # Use a short random name to leave space for the socket filename.
            name = ".syc-" + uuid4().hex[:16]
            os.mkdir(name, 0o700, dir_fd=parent)
            try:
                child = os.open(name, flags, dir_fd=parent)
                try:
                    os.fchmod(child, 0o700)
                    info = os.fstat(child)
                    if (
                        info.st_uid != os.geteuid()
                        or stat.S_IMODE(info.st_mode) != 0o700
                    ):
                        raise PermissionError("UDS session directory is not private")
                    self._identity = (info.st_dev, info.st_ino)
                finally:
                    os.close(child)
            except BaseException:
                os.rmdir(name, dir_fd=parent)
                raise
            self.path = path / name
            self._parent = parent
            self._name = name
            parent = None
        finally:
            if parent is not None:
                os.close(parent)

    @staticmethod
    def _check_ancestor(info):
        writable = info.st_mode & 0o022
        if info.st_uid not in (0, os.geteuid()) or (
            writable and not (info.st_uid == 0 and info.st_mode & stat.S_ISVTX)
        ):
            raise PermissionError("Unsafe UDS directory ancestor")

    def close(self):
        """Remove the original directory only if it still exists and is empty."""
        if self._parent is None:
            return
        try:
            try:
                info = os.stat(self._name, dir_fd=self._parent, follow_symlinks=False)
            except FileNotFoundError:
                return
            if (info.st_dev, info.st_ino) != self._identity:
                return
            try:
                os.rmdir(self._name, dir_fd=self._parent)
            except OSError:
                # Preserve nonempty directories and report cleanup failure.
                raise
        finally:
            os.close(self._parent)
            self._parent = None
