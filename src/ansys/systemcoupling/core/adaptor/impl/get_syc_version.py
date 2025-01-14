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

# This is the version we assume if no GetVersion query is available from
# the SyC server.
_FALLBACK_VERSION = "23.1"


def get_syc_version(api) -> str:
    """Get the System Coupling version.

    The version is returned in a string like ``"23.2"``.

    System Coupling versions earlier than 23.2 (2023 R2) do not expose
    the ``GetVersion`` query. Because the first version of the server
    that PySystemCoupling is able to connect to is 23.1 (2023 R1), the
    version is assumed to be 23.1 if no version query exists.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling *native API* .
    """

    def clean_version_string(version_in: str) -> str:
        year, _, release = version_in.partition(" ")
        if len(year) == 4 and year.startswith("20") and release.startswith("R"):
            try:
                year = int(year[2:])
                release = int(release[1:])
                return f"{year}.{release}"
            except:
                pass
        raise RuntimeError(
            f"Version string {version_in} has invalid format (expect '20yy Rn')."
        )

    cmds = api.GetCommandAndQueryMetadata()
    exists = any(cmd["name"] == "GetVersion" for cmd in cmds)
    return clean_version_string(api.GetVersion()) if exists else _FALLBACK_VERSION
