"""Logging module.

This module provides a basic general framework for logging in pySystemCoupling.
"""

# NOTE: The starting point for this module is the pyfluent logger.
#       Unlike the pymapdl logger, this does not support instance-specific
#       logging. Over time, we may want to adopt some of the mapdl approach.


import logging
import os
from pathlib import Path
import tempfile
from typing import Any


class Logger:
    """Logger class.

    Methods
    -------
    set_level(level)
        Set logging level
    log_to_stdout()
        Enable logging to stdout
    disable_log_to_stdout()
        Disable logging to stdout
    log_to_file(filepath)
        Enable logging to file
    disable_log_to_file()
        Disable logging to file
    """

    def __init__(self, level: Any = logging.ERROR):
        self.logger = logging.getLogger()
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
        """Set logging level.

        Parameters
        ----------
        level : Any
            Any of the logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG)
            in string or enum format
        """
        self.logger.setLevel(level)

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
        """Enable logging to file.

        Only a single file logging handler may be active at any time. If a file logger is
        already enabled, calling this with a different filepath will
        switch file logging to the new file.

        Parameters
        ----------
        filepath : str, optional
            path to log file. If a filepath is not passed, a default filepath will be chosen
            unless the logger already logs to a file, in which case this call will be ignored.
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
        """Disable logging to file."""
        self.logger.removeHandler(self.file_handler)


LOG = Logger()
