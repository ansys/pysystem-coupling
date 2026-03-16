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

from ansys.systemcoupling.core.syc_version import (
    SycVersion,
    compare_versions,
    normalize_version,
)


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


def test_compare_versions() -> None:
    # Test equal versions
    assert compare_versions("25.1", "25.1") == 0
    assert compare_versions("251", "25_1") == 0
    assert compare_versions("24.2", "242") == 0

    # Test version a > version b
    assert compare_versions("25.2", "25.1") > 0
    assert compare_versions("25.1", "24.2") > 0
    assert compare_versions("26.1", "25.2") > 0

    # Test version a < version b
    assert compare_versions("25.1", "25.2") < 0
    assert compare_versions("24.2", "25.1") < 0
    assert compare_versions("25.2", "26.1") < 0

    # Test different formats
    assert compare_versions("252", "25.1") > 0
    assert compare_versions("24_2", "25.1") < 0


def test_syc_version_enum_values() -> None:
    """Test that SycVersion enum contains expected version values."""
    # Test enum creation from string
    assert SycVersion("27.1") == SycVersion.v271
    assert SycVersion("26.1") == SycVersion.v261
    assert SycVersion("25.2") == SycVersion.v252
    assert SycVersion("25.1") == SycVersion.v251
    assert SycVersion("24.2") == SycVersion.v242

    # Test enum values
    assert SycVersion.v271.value == "27.1"
    assert SycVersion.v261.value == "26.1"
    assert SycVersion.v252.value == "25.2"
    assert SycVersion.v251.value == "25.1"
    assert SycVersion.v242.value == "24.2"


def test_syc_version_number_property() -> None:
    """Test the number property of SycVersion enum."""
    assert SycVersion.v271.number == 271
    assert SycVersion.v261.number == 261
    assert SycVersion.v252.number == 252
    assert SycVersion.v251.number == 251
    assert SycVersion.v242.number == 242


def test_syc_version_awp_var_property() -> None:
    """Test the awp_var property of SycVersion enum."""
    assert SycVersion.v271.awp_var == "AWP_ROOT271"
    assert SycVersion.v261.awp_var == "AWP_ROOT261"
    assert SycVersion.v252.awp_var == "AWP_ROOT252"
    assert SycVersion.v251.awp_var == "AWP_ROOT251"
    assert SycVersion.v242.awp_var == "AWP_ROOT242"


def test_syc_version_vstring_property() -> None:
    """Test the vstring property of SycVersion enum."""
    assert SycVersion.v271.v_string == "v271"
    assert SycVersion.v261.v_string == "v261"
    assert SycVersion.v252.v_string == "v252"
    assert SycVersion.v251.v_string == "v251"
    assert SycVersion.v242.v_string == "v242"


def test_syc_version_uscore_form_property() -> None:
    """Test the uscore_form property of SycVersion enum."""
    assert SycVersion.v271.uscore_string == "27_1"
    assert SycVersion.v261.uscore_string == "26_1"
    assert SycVersion.v252.uscore_string == "25_2"
    assert SycVersion.v251.uscore_string == "25_1"
    assert SycVersion.v242.uscore_string == "24_2"


def test_syc_version_major_minor_tuple_property() -> None:
    """Test the major_minor_tuple property of SycVersion enum."""
    assert SycVersion.v271.major_minor_tuple == (27, 1)
    assert SycVersion.v261.major_minor_tuple == (26, 1)
    assert SycVersion.v252.major_minor_tuple == (25, 2)
    assert SycVersion.v251.major_minor_tuple == (25, 1)
    assert SycVersion.v242.major_minor_tuple == (24, 2)


def test_syc_version_minimum_supported() -> None:
    """Test the minimum_supported class method."""
    min_version = SycVersion.minimum_supported()
    assert min_version == SycVersion.v242
    assert min_version.value == "24.2"
    assert min_version.number == 242


def test_syc_version_invalid() -> None:
    """Test that creating SycVersion with invalid version raises ValueError."""
    with pytest.raises(ValueError):
        SycVersion("23.1")
    with pytest.raises(ValueError):
        SycVersion("28.1")
    with pytest.raises(ValueError):
        SycVersion("invalid")


def test_syc_version_all_members() -> None:
    """Test that all enum members are accessible and ordered correctly."""
    all_versions = list(SycVersion)
    expected_versions = [
        SycVersion.v271,
        SycVersion.v261,
        SycVersion.v252,
        SycVersion.v251,
        SycVersion.v242,
    ]
    assert all_versions == expected_versions

    # Test that versions are in descending order by number
    numbers = [version.number for version in all_versions]
    assert numbers == sorted(numbers, reverse=True)
