# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Logging module.

This module provides a basic framework for logging in PySystemCoupling.
"""

# NOTE: The starting point for this module is the PyFluent logger.
#       Unlike the PyMAPDL logger, this logger does not support instance-specific
#       logging. Over time, we may want to adopt some of the MAPDL approach.


import logging
import os
from pathlib import Path
import tempfile
from typing import Any


class Logger:
    """Provides the basic logging framework.

    Methods
    -------
    set_level(level)
        Set the logging level.
    log_to_stdout()
        Enable logging to stdout.
    disable_log_to_stdout()
        Disable logging to stdout.
    log_to_file(filepath)
        Enable logging to a file.
    disable_log_to_file()
        Disable logging to a file.
    """

    def __init__(self, level: Any = logging.ERROR):
        self.logger = logging.getLogger("pysystem-coupling")
        self.stream_handler = None
        self.file_handler = None
        self.log_filepath = None
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        self.log_to_stdout()
        self.logger.setLevel(level)

        # Writing logging methods.
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.log = self.logger.log

    def set_level(self, level: Any) -> None:
        """Set the logging level.

        Parameters
        ----------
        level : Any
            Logging level in string or enum format. Options are ``CRITICAL``,
            ``ERROR``, ``WARNING``, ``INFO,`` and ``DEBUG``.
        """
        self.logger.setLevel(level)

    @property
    def current_level(self) -> Any:
        return self.logger.level

    def _get_default_log_filepath(self):
        fd, filepath = tempfile.mkstemp(
            suffix=f"-{os.getpid()}.txt",
            prefix="pysyc-",
            dir=str(Path.cwd()),
        )
        os.close(fd)
        return Path(filepath)

    def log_to_stdout(self) -> None:
        """Enable logging to stdout."""
        if self.stream_handler is None:
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def disable_log_to_stdout(self) -> None:
        """Disable logging to stdout."""
        if self.stream_handler is not None:
            self.logger.removeHandler(self.stream_handler)
            self.stream_handler = None

    def log_to_file(self, filepath: str = None) -> None:
        """Enable logging to a file.

        Only a single file logging handler may be active at any time. If a file logger is
        already enabled, calling this with a different filepath switches file logging to
        the new file.

        Parameters
        ----------
        filepath : str, optional
            Path to log file. If a filepath is not passed, a default filepath is chosen
            unless the logger already logs to a file, in which case, this call is ignored.
        """
        if not filepath and not self.log_filepath:
            self.log_filepath = self._get_default_log_filepath()
        elif filepath and (not self.log_filepath or self.log_filepath == filepath):
            self.log_filepath = Path(filepath)
        else:
            # retain current handler
            return
        self.logger.removeHandler(self.file_handler)
        self.file_handler = logging.FileHandler(self.log_filepath)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def disable_log_to_file(self) -> None:
        """Disable logging to a file."""
        self.logger.removeHandler(self.file_handler)


LOG = Logger()
