# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

import pytest

"""``datamodel_metadata`` is the datamodel API that plays a role in the "native" API."""

from ansys.systemcoupling.core.native_api.datamodel_metadata import (
    build as build_metadata,
)
from dm_raw_metadata import dm_metadata


@pytest.fixture(name="metadata")
def _metadata():
    return build_metadata(dm_metadata)


def test_is_object_path(metadata) -> None:
    assert metadata.is_object_path("/SystemCoupling/Library")
    assert metadata.is_object_path("/SystemCoupling/CouplingInterface:intf1")
    assert metadata.is_object_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt"
    )


def test_is_object_path_failure(metadata) -> None:
    assert not metadata.is_object_path("/Bob")
    assert not metadata.is_object_path("/SystemCoupling/Library/Bob")
    assert not metadata.is_object_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Value"
    )


def test_is_parameter_path(metadata) -> None:
    assert metadata.is_parameter_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Value"
    )
    assert metadata.is_parameter_path("/SystemCoupling/ActivateHidden/BetaFeatures")


def test_is_parameter_path_failure(metadata) -> None:
    assert not metadata.is_parameter_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Bob"
    )
    assert not metadata.is_parameter_path(
        "/SystemCoupling/CouplingInterface:intf1/Bob:dt/Value"
    )
    assert not metadata.is_parameter_path("/SystemCoupling/Library")


def test_is_named_object_path(metadata) -> None:
    assert not metadata.is_named_object_path("/SystemCoupling/Library")
    assert metadata.is_named_object_path("/SystemCoupling/CouplingInterface:intf1")
    assert not metadata.is_named_object_path(
        "/SystemCoupling/CouplingInterface:intf1/DataTransfer:dt/Stabilization"
    )
    assert not metadata.is_named_object_path(
        "/SystemCoupling/CouplingInterface:intf1/Bob:dt"
    )
