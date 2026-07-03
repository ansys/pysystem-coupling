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

from typing import Callable, Protocol

from ansys.systemcoupling.core.adaptor.impl.injected_commands_cosim import (
    CosimInjectedCommandsProvider,
    get_injected_cmd_data,
)
from ansys.systemcoupling.core.adaptor.impl.session_protocol import SessionProtocol
from ansys.systemcoupling.core.types import SystemCouplingMode


class InjectedCommandsProvider(Protocol):
    def get_injected_cmd_map(
        self,
        category: str,
    ) -> dict[str, Callable]:
        """Method to get a dictionary mapping names
        to functions that implement injected commands for the specified API
        category.
        """
        ...


class DefaultInjectedCommandsProvider(InjectedCommandsProvider):
    def get_injected_cmd_map(
        self,
        category: str,
    ) -> dict[str, Callable]:
        """Default implementation of the method to get a dictionary mapping names
        to functions that implement injected commands for the specified API
        category. This default implementation returns an empty dictionary.
        """
        return {}


def get_injected_cmd_metadata(mode: SystemCouplingMode) -> list:
    if mode == SystemCouplingMode.COSIM:
        return get_injected_cmd_data()
    else:
        return []


def get_commands_for_mode(
    mode: SystemCouplingMode, version: str, session: SessionProtocol, rpc
) -> InjectedCommandsProvider:
    if mode == SystemCouplingMode.COSIM:
        return CosimInjectedCommandsProvider(version, session, rpc)
    else:
        return DefaultInjectedCommandsProvider()
