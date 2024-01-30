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

#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class partition_participants(Command):
    """
    'partition_participants' child.

    Parameters
    ----------
    algorithm_name : str, optional
        'algorithm_name' child.
    machine_list : typing.List[typing.Dict[str, typing.Union[str, int]]], optional
        'machine_list' child.
    names_and_fractions : typing.List[typing.Tuple[str, float]], optional
        'names_and_fractions' child.

    """

    syc_name = "PartitionParticipants"

    argument_names = ["algorithm_name", "machine_list", "names_and_fractions"]

    class algorithm_name(String):
        """
        'algorithm_name' child.
        """

        syc_name = "AlgorithmName"

    class machine_list(StrOrIntDictList):
        """
        'machine_list' child.
        """

        syc_name = "MachineList"

    class names_and_fractions(StrFloatPairList):
        """
        'names_and_fractions' child.
        """

        syc_name = "NamesAndFractions"
