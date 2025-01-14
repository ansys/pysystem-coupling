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

import pytest

from ansys.systemcoupling.core.util.state_keys import (
    adapt_client_named_object_keys,
    adapt_native_named_object_keys,
    adapt_native_named_object_keys_in_place,
)


@pytest.mark.parametrize(
    "state_in, expected",
    [
        ({}, {}),
        ({"A": None}, {"A": None}),
        ({"A": {}}, {"A": {}}),
        ({"A": {"p": 2}}, {"A": {"p": 2}}),
        (
            {"A:a": {"B": {"C:c1": {"p": 1, "q": 2}, "C:c2": {"p": 2, "s": "bob"}}}},
            {
                "A": {
                    "a": {
                        "B": {"C": {"c1": {"p": 1, "q": 2}, "c2": {"p": 2, "s": "bob"}}}
                    }
                }
            },
        ),
        (
            {
                "A:a1": {"B": {"C:c1": {"p": 1, "q": 2}, "C:c2": {"p": 2, "s": "bob"}}},
                "A:a2": {
                    "B": {"C:c1": {"p": 666, "q": 42}, "C:c3": {"p": 2, "s": "fred"}}
                },
            },
            {
                "A": {
                    "a1": {
                        "B": {"C": {"c1": {"p": 1, "q": 2}, "c2": {"p": 2, "s": "bob"}}}
                    },
                    "a2": {
                        "B": {
                            "C": {
                                "c1": {"p": 666, "q": 42},
                                "c3": {"p": 2, "s": "fred"},
                            }
                        }
                    },
                }
            },
        ),
    ],
)
def test_adapt_native_named_object_keys(state_in, expected):
    assert adapt_native_named_object_keys(state_in) == expected


@pytest.mark.parametrize(
    "state_in, expected",
    [
        ({}, {}),
        ({"A": None}, {"A": None}),
        ({"A": {}}, {"A": {}}),
        ({"A": {"p": 2}}, {"A": {"p": 2}}),
        (
            {"A:a": {"B": {"C:c1": {"p": 1, "q": 2}, "C:c2": {"p": 2, "s": "bob"}}}},
            {
                "A": {
                    "a": {
                        "B": {"C": {"c1": {"p": 1, "q": 2}, "c2": {"p": 2, "s": "bob"}}}
                    }
                }
            },
        ),
        (
            {
                "A:a1": {"B": {"C:c1": {"p": 1, "q": 2}, "C:c2": {"p": 2, "s": "bob"}}},
                "A:a2": {
                    "B": {"C:c1": {"p": 666, "q": 42}, "C:c3": {"p": 2, "s": "fred"}}
                },
            },
            {
                "A": {
                    "a1": {
                        "B": {"C": {"c1": {"p": 1, "q": 2}, "c2": {"p": 2, "s": "bob"}}}
                    },
                    "a2": {
                        "B": {
                            "C": {
                                "c1": {"p": 666, "q": 42},
                                "c3": {"p": 2, "s": "fred"},
                            }
                        }
                    },
                }
            },
        ),
    ],
)
def test_adapt_native_named_object_keys_in_place(state_in, expected):
    adapt_native_named_object_keys_in_place(state_in)
    assert state_in == expected


@pytest.mark.parametrize(
    "state_in, expected",
    [
        ({}, {}),
        ({"X": {}}, {"X": {}}),
        ({"X": {"p": 2}}, {"X": {"p": 2}}),
        (
            {
                "A": {
                    "a": {
                        "B": {"C": {"c1": {"p": 1, "q": 2}, "c2": {"p": 2, "s": "bob"}}}
                    }
                }
            },
            {"A:a": {"B": {"C:c1": {"p": 1, "q": 2}, "C:c2": {"p": 2, "s": "bob"}}}},
        ),
        (
            {
                "A": {
                    "a1": {
                        "B": {"C": {"c1": {"p": 1, "q": 2}, "c2": {"p": 2, "s": "bob"}}}
                    },
                    "a2": {
                        "B": {
                            "C": {
                                "c1": {"p": 666, "q": 42},
                                "c3": {"p": 2, "s": "fred"},
                            }
                        }
                    },
                }
            },
            {
                "A:a1": {"B": {"C:c1": {"p": 1, "q": 2}, "C:c2": {"p": 2, "s": "bob"}}},
                "A:a2": {
                    "B": {"C:c1": {"p": 666, "q": 42}, "C:c3": {"p": 2, "s": "fred"}}
                },
            },
        ),
    ],
)
def test_adapt_client_named_object_keys(state_in, expected):
    level_named = {0: {"A"}, 2: {"C"}}
    assert (
        adapt_client_named_object_keys(state_in, level_type_map=level_named) == expected
    )
