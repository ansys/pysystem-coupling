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

#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class add_participant(Command):
    """
    'add_participant' child.

    Parameters
    ----------
    additional_arguments : str, optional
        'additional_arguments' child.
    executable : str, optional
        'executable' child.
    input_file : str, optional
        'input_file' child.
    participant_type : str, optional
        'participant_type' child.
    working_directory : str, optional
        'working_directory' child.

    """

    syc_name = "AddParticipant"

    argument_names = [
        "additional_arguments",
        "executable",
        "input_file",
        "participant_type",
        "working_directory",
    ]

    class additional_arguments(String):
        """
        'additional_arguments' child.
        """

        syc_name = "AdditionalArguments"

    class executable(String):
        """
        'executable' child.
        """

        syc_name = "Executable"

    class input_file(String):
        """
        'input_file' child.
        """

        syc_name = "InputFile"

    class participant_type(String):
        """
        'participant_type' child.
        """

        syc_name = "ParticipantType"

    class working_directory(String):
        """
        'working_directory' child.
        """

        syc_name = "WorkingDirectory"
