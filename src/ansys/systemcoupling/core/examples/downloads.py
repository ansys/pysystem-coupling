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

"""Functions to download sample datasets from the PyAnsys data repository.

Examples
--------

>>> from ansys.systemcoupling.core import examples
>>> filename = examples.download_file("mapdl.scp", "oscillating_plate_fluent")
>>> filename
'/home/user/.local/share/ansys_systemcoupling_core/examples/mapdl.scp'
"""

import os
import pathlib
import shutil
from typing import Optional
import urllib.request
import zipfile

import ansys.systemcoupling.core as pysyc


def get_ext(filename: str) -> str:
    """Extract the extension of a file."""
    ext = os.path.splitext(filename)[1].lower()
    return ext


def delete_downloads() -> bool:
    """Delete all downloaded examples to free space or update the files."""
    shutil.rmtree(pysyc.EXAMPLES_PATH)
    os.makedirs(pysyc.EXAMPLES_PATH)
    return True


def _decompress(filename: str) -> None:
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall(pysyc.EXAMPLES_PATH)
    return zip_ref.close()


def _get_file_url(filename: str, directory: Optional[str] = None) -> str:
    root_url = "https://github.com/ansys/example-data/raw/master/"
    # root_url = "https://github.com/ansys/pysystem-coupling/raw/feature/more_doc/"
    if directory:
        return f"{root_url}" f"{directory}/{filename}"
    return f"{root_url}/{filename}"


def _retrieve_file(url: str, filename: str, download_to_cwd: bool = False):

    name_to_return = lambda local_path: (
        local_path if not download_to_cwd else pathlib.Path(local_path).name
    )

    download_target_dir = "." if download_to_cwd else pysyc.EXAMPLES_PATH

    # First check if file has already been downloaded
    local_path = os.path.join(download_target_dir, os.path.basename(filename))
    local_path_no_zip = local_path.replace(".zip", "")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return name_to_return(local_path_no_zip), None

    # grab the correct url retriever
    urlretrieve = urllib.request.urlretrieve

    # Perform download
    saved_file, resp = urlretrieve(url)
    shutil.move(saved_file, local_path)
    if get_ext(local_path) in [".zip"]:
        _decompress(local_path)
        local_path = local_path[:-4]
    return name_to_return(local_path), resp


def download_file(filename: str, directory: Optional[str] = None):
    url = _get_file_url(filename, directory)
    download_to_cwd = (
        os.getenv("PYSYC_BUILD_SPHINX_GALLERY") == "1"
        and os.getenv("SYC_LAUNCH_CONTAINER") == "1"
    )
    return _retrieve_file(url, filename, download_to_cwd)[0]
