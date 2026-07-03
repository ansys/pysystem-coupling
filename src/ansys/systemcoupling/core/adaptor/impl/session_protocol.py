# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

from typing import Optional, Protocol

from ansys.systemcoupling.core.charts.plot_functions import (
    GrpcDataSourceProtocol,
)
from ansys.systemcoupling.core.native_api import NativeApi

from .types import Container


class SessionProtocol(Protocol):
    """For use when we cannot import Session directly because of potential
    circular imports; defines a protocol for typing.

    It is mainly used as a means of accessing the "API roots".
    """

    case: Container
    setup: Container
    solution: Container
    _native_api: NativeApi

    def download_file(
        self, file_name: str, local_file_dir: str = ".", overwrite: bool = False
    ) -> None: ...

    def upload_file(
        self,
        file_name: str,
        remote_file_name: Optional[str] = None,
        overwrite: bool = False,
    ) -> None: ...

    def _grpc(self) -> GrpcDataSourceProtocol: ...
