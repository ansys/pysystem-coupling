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


def assert_(condition: bool, failure_msg: str = ""):
    """Function that can be used to replace ``assert`` statements in code.

    Assertions are not always preserved in run-time code and some tools will
    warn about their use. However, sometimes the use of an assertion seems
    appropriate to indicate something that should "never happen", such as
    when used to confirm an invariant or a pre- or post-condition.

    This function can be used in place of an ``assert`` statement and raises
    an exception if the provided boolean is ``False``. Since only ``assert``
    itself should raise an ``AssertionError``, ``RuntimeError`` is raised
    here.
    """
    if not condition:
        raise RuntimeError(failure_msg or "Assertion failed")
