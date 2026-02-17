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

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from ansys.systemcoupling.core.client.syc_launch_script import (
    _SCRIPT_NAME,
    path_to_system_coupling,
)


class TestPathToSystemCoupling:
    """Test suite for path_to_system_coupling function."""

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {"SYSC_ROOT": "/opt/ansys/sysc"}, clear=True)
    def test_sysc_root_env_var_set(self, mock_is_file):
        """Test when SYSC_ROOT environment variable is set."""
        mock_is_file.return_value = True

        result = path_to_system_coupling(None)

        # Use pathlib.Path for cross-platform compatibility
        expected = str(Path("/opt/ansys/sysc") / "bin" / _SCRIPT_NAME)
        assert result == expected
        # Verify that is_file was called
        mock_is_file.assert_called()

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {"SYSC_ROOT": "/opt/ansys/sysc"}, clear=True)
    def test_sysc_root_env_var_set_windows(self, mock_is_file):
        """Test when SYSC_ROOT is set on Windows."""
        mock_is_file.return_value = True

        with patch(
            "ansys.systemcoupling.core.client.syc_launch_script._IS_WINDOWS", True
        ):
            with patch(
                "ansys.systemcoupling.core.client.syc_launch_script._SCRIPT_NAME",
                "systemcoupling.bat",
            ):
                result = path_to_system_coupling(None)

        expected = str(Path("/opt/ansys/sysc") / "bin" / "systemcoupling.bat")
        assert result == expected

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {"AWP_ROOT": "/opt/ansys/v252"}, clear=True)
    def test_awp_root_env_var_set(self, mock_is_file):
        """Test when AWP_ROOT environment variable is set."""
        mock_is_file.return_value = True

        result = path_to_system_coupling(None)

        expected = str(
            Path("/opt/ansys/v252") / "SystemCoupling" / "bin" / _SCRIPT_NAME
        )
        assert result == expected

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {"AWP_ROOT252": "/opt/ansys/v252"}, clear=True)
    def test_version_specific_awp_root(self, mock_is_file):
        """Test when version-specific AWP_ROOT variable is set."""
        mock_is_file.return_value = True

        result = path_to_system_coupling("25.2")

        expected = str(
            Path("/opt/ansys/v252") / "SystemCoupling" / "bin" / _SCRIPT_NAME
        )
        assert result == expected

    @patch("pathlib.Path.is_file")
    @patch.dict(
        os.environ,
        {"AWP_ROOT271": "C:/opt/ansys/v271", "AWP_ROOT252": "C:/opt/ansys/v252"},
        clear=True,
    )
    def test_latest_version_discovery(self, mock_path_is_file):
        """Test automatic discovery of latest installed version."""
        # Mock Path.is_file() to return True for the first version checked (v271)
        mock_path_is_file.return_value = True

        result = path_to_system_coupling(None)

        # Normalize path separators and use Windows-style paths
        expected = str(
            Path("C:/opt/ansys/v271") / "SystemCoupling" / "bin" / _SCRIPT_NAME
        )
        actual = str(Path(result))
        assert actual == expected

    @patch.dict(os.environ, {}, clear=True)
    def test_no_installation_found(self):
        """Test error when no System Coupling installation is found."""
        with pytest.raises(
            RuntimeError, match="Failed to locate System Coupling from environment"
        ):
            path_to_system_coupling(None)

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {"SYSC_ROOT": "/opt/ansys/sysc"}, clear=True)
    def test_script_does_not_exist(self, mock_is_file):
        """Test error when script path doesn't exist."""
        mock_is_file.return_value = False

        with pytest.raises(RuntimeError, match="System Coupling script does not exist"):
            path_to_system_coupling(None)

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {"AWP_ROOT": "/opt/ansys/v251"}, clear=True)
    def test_version_consistency_check_success(self, mock_is_file):
        """Test successful version consistency check."""
        mock_is_file.return_value = True

        # This should not raise an error since v251 is consistent with 25.1
        result = path_to_system_coupling("25.1")

        expected = str(
            Path("/opt/ansys/v251") / "SystemCoupling" / "bin" / _SCRIPT_NAME
        )
        assert result == expected

    @patch.dict(os.environ, {"AWP_ROOT": "/opt/ansys/v252"}, clear=True)
    def test_version_consistency_check_failure(self):
        """Test version consistency check failure."""
        # Should raise error since v252 is inconsistent with requested 25.1
        with pytest.raises(
            RuntimeError, match="The specified version string '25.1' is inconsistent"
        ):
            path_to_system_coupling("25.1")

    @patch("pathlib.Path.is_file")
    @patch.dict(
        os.environ,
        {"SYSC_ROOT": "/opt/ansys/sysc", "AWP_ROOT": "/opt/ansys/v252"},
        clear=True,
    )
    def test_explicit_version_with_env_vars_warning(self, mock_is_file):
        """Test warning when explicit version is provided with environment variables set."""
        mock_is_file.return_value = True

        # Mock the logger to capture the warning
        with patch(
            "ansys.systemcoupling.core.client.syc_launch_script.LOG.warning"
        ) as mock_log:
            path_to_system_coupling("25.2")

        # Verify the warning was called
        mock_log.assert_called_once()
        call_args = mock_log.call_args[0][0]
        assert "An explicit version" in call_args
        assert "has been specified for launching System Coupling" in call_args

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {"AWP_ROOT242": "/opt/ansys/v242"}, clear=True)
    def test_specific_version_lookup(self, mock_is_file):
        """Test lookup of specific version."""
        mock_is_file.return_value = True

        result = path_to_system_coupling("24.2")

        expected = str(
            Path("/opt/ansys/v242") / "SystemCoupling" / "bin" / _SCRIPT_NAME
        )
        assert result == expected

    @patch("pathlib.Path.is_file")
    @patch.dict(os.environ, {}, clear=True)
    def test_version_not_found(self, mock_is_file):
        """Test error when requested version is not found."""
        with pytest.raises(
            RuntimeError, match="Failed to locate System Coupling from environment"
        ):
            path_to_system_coupling("99.9")

    @patch("pathlib.Path.is_file")
    @patch.dict(
        os.environ,
        {"AWP_ROOT252": "C:/opt/ansys/v252", "AWP_ROOT251": "C:/opt/ansys/v251"},
        clear=True,
    )
    def test_latest_version_discovery_order(self, mock_path_is_file):
        """Test that latest version discovery finds the highest version."""
        # Mock to return True only for the first version found (should be v252, the highest)
        # This simulates finding a valid installation at the first location checked
        mock_path_is_file.return_value = True

        result = path_to_system_coupling(None)

        # Should find v252 (higher version) as it's checked first
        expected = str(
            Path("C:/opt/ansys/v252") / "SystemCoupling" / "bin" / _SCRIPT_NAME
        )
        actual = str(Path(result))
        assert actual == expected

    def test_normalize_version_integration(self):
        """Test that version normalization works correctly with various formats."""
        test_cases = [
            ("25.2", "25.2"),
            ("252", "25.2"),
            ("25_2", "25.2"),
            ("v252", "25.2"),
        ]

        for input_version, expected_normalized in test_cases:
            with patch("pathlib.Path.is_file", return_value=True):
                with patch.dict(
                    os.environ, {"AWP_ROOT252": "/opt/ansys/v252"}, clear=True
                ):
                    result = path_to_system_coupling(input_version)
                    expected = str(
                        Path("/opt/ansys/v252")
                        / "SystemCoupling"
                        / "bin"
                        / _SCRIPT_NAME
                    )
                    assert result == expected
