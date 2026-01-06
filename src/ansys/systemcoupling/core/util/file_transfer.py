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
import shutil
from typing import Any, Optional, Protocol


# Note: generally exclude items in this file from coverage for now
class FileTransferService(Protocol):  # pragma: no cover
    def upload_file(
        self, file_name: str, remote_file_name: Optional[str], overwrite: bool
    ) -> str: ...

    def download_file(self, file_name: str, local_file_dir: str, overwrite: bool): ...


class NullFileTransferService(FileTransferService):  # pragma: no cover
    """An essentially do-nothing implementation of file upload/download
    service (with a minimal ``upload_file`` implementation)."""

    def upload_file(
        self, file_name: str, remote_file_name: Optional[str], overwrite: bool
    ) -> str:
        # TODO - what should the behaviour be if remote_file_name is not None?
        # It is not obvious that it would even make sense to call the Null
        # implementation in that case.
        return file_name


class PimFileTransferService:  # pragma: no cover
    """Provides a file upload and download service for the case when PySystemCoupling
    is running as a remote instance managed by
    `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

    Currently for internal use only.

    """

    def __init__(self, pim_instance: Any):

        self.pim_instance = pim_instance
        self.file_service = None

        try:
            upload_server = self.pim_instance.services["http-simple-upload-server"]
        except KeyError:
            raise RuntimeError("PIM instance is not configured with the upload service")
        else:
            # This import is available in the Ansys Lab environment
            from simple_upload_server.client import Client

            # Exclude Bandit check. Hardcoded token only used in constrained Ansys Lab environment.
            self.file_service = Client(  # nosec B106
                token="token",
                url=upload_server.uri,
                headers=upload_server.headers,
            )

    def upload_file(
        self, file_name: str, remote_file_name: Optional[str], overwrite: bool
    ) -> str:
        """Upload a file to the PIM-managed instance.

        The remote file may optionally be given a different name from the local one.

        If the local file name includes a directory path, this is stripped and the
        remote file is always placed in the "working directory" of the container.

        Unless ``overwrite`` is ``True``, a ``FileExistsError`` will be raised if
        the remote file already exists.

        Parameters
        ----------
        file_name : str
            local file name
        remote_file_name : str or None
            remote file name (or use local file name if None)
        overwrite: bool
            whether to overwrite the remote file if it already exists

        Returns
        -------
        str
            The name assigned to the remote file name. If ``file_name`` included
            a directory prefix, this is stripped from the returned name.
        """
        if os.path.isfile(file_name):
            remote_file_name = remote_file_name or os.path.basename(file_name)
            delete_copy = False
            if os.path.dirname(file_name):
                base_filename = os.path.basename(file_name)
                dst_file = base_filename
                dst_file_footer = 0
                while os.path.exists(dst_file):
                    dst_file_footer += 1
                    dst_file = f"{base_filename}_{dst_file_footer}"
                shutil.copy2(file_name, dst_file)
                delete_copy = True
                file_name = dst_file
            if not overwrite and self.file_service.file_exist(remote_file_name):
                raise FileExistsError(f"{remote_file_name} already exists remotely.")
            self.file_service.upload_file(file_name, remote_file_name)
            if delete_copy:
                os.remove(file_name)
            return remote_file_name
        else:
            raise FileNotFoundError(f"Local file {file_name} does not exist.")

    def download_file(self, file_name: str, local_file_dir: str, overwrite: bool):
        """Download a file from the PIM-managed instance.

        Unless ``overwrite`` is ``True``, a ``FileExistsError`` will be raised if
        the local file already exists.

        Parameters
        ----------
        file_name : str
            file name
        local_file_dir : str
            local directory to write the file
        overwrite : bool
            whether to overwrite the remote file if it already exists
        """
        if self.file_service.file_exist(file_name):
            if not overwrite:
                local_file_path = os.path.join(local_file_dir, file_name)
                if os.path.isfile(local_file_path):
                    raise FileExistsError(
                        f"Local file {local_file_path} already exists."
                    )
            self.file_service.download_file(file_name, local_file_dir)
        else:
            raise FileNotFoundError(f"Remote file {file_name} does not exist.")


def file_transfer_service(
    pim_instance: Optional[Any] = None,
) -> FileTransferService:  # pragma: no cover
    """If a ``PIM`` instance is provided, returns an object providing remote
    file upload and download, otherwise returns a 'no-op' version of the object.
    """
    if pim_instance:
        return PimFileTransferService(pim_instance)
    else:
        return NullFileTransferService()
