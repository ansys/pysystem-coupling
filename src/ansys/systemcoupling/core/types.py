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

"""Core types and enums for PySystemCoupling."""

from enum import Enum


class SystemCouplingMode(str, Enum):
    """System Coupling execution modes.

    Defines the available modes for launching and running System Coupling,
    which affect the available API surface and functionality.
    """

    COSIM = "cosim"
    """Co-simulation mode (default). Provides the full API including
    participant management and injected commands."""

    FILEIO = "fileio"
    """File I/O mode. Provides basic API without participant management
    or co-simulation specific features."""

    def to_startup_argument(self) -> str:
        """Convert the mode to the argument value used when launching System Coupling.

        This centralizes the mapping logic where some logical modes need to be
        converted to different startup argument values.

        Returns
        -------
        str
            The argument value to pass to System Coupling with the -m flag.
        """
        if self == SystemCouplingMode.COSIM:
            return "cosimgui"
        else:
            return self.value
