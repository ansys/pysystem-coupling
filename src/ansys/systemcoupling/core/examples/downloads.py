# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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


def _retrieve_file(url: str, filename: str):
    # First check if file has already been downloaded
    local_path = os.path.join(pysyc.EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace(".zip", "")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip, None

    # grab the correct url retriever
    urlretrieve = urllib.request.urlretrieve

    # Perform download
    saved_file, resp = urlretrieve(url)
    shutil.move(saved_file, local_path)
    if get_ext(local_path) in [".zip"]:
        _decompress(local_path)
        local_path = local_path[:-4]
    return local_path, resp


def _temp_get_file(filename: str, directory: Optional[str] = None):
    example_dir = os.environ.get("PYSYC_EXAMPLE_DIR")
    if example_dir is None:
        raise Exception(
            "PYSYC_EXAMPLE_DIR is not set. "
            "(This is a temporary requirement during development.)"
        )
    local_path = os.path.join(pysyc.EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace(".zip", "")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip

    file_path = os.path.join(example_dir, directory, filename)
    shutil.copy(file_path, local_path)
    if get_ext(local_path) in [".zip"]:
        _decompress(local_path)
        local_path = local_path[:-4]
    return local_path


def download_file(filename: str, directory: Optional[str] = None):
    url = _get_file_url(filename, directory)
    return _retrieve_file(url, filename)[0]
    # return _temp_get_file(filename, directory)
