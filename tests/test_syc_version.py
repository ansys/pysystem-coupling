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
