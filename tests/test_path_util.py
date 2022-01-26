import pytest

from ansys.systemcoupling.core.path_util import (to_typelist, to_typepath,
                                                 join_path_strs)

@pytest.mark.parametrize("path, expected",
                         [("/a", "/a"), ("/a/b:b1", "/a/b"),
                          ("/a:a1", "/a"), ("/", "/"),
                          ("", "")])
def test_to_typepath(path, expected):
    assert to_typepath(path) == expected

@pytest.mark.parametrize("path, expected",
                         [("/a", ["a"]), ("/a/b:b1", ["a", "b"]),
                          ("/a:a1", ["a"]), ("/", ['']),
                          ("", [])])
def test_to_typelist(path, expected):
    assert to_typelist(path) == expected

@pytest.mark.parametrize("strs, expected",
                         [(("a",), "a"), (("/a", "b"), "/a/b"),
                          (("a", "b"), "a/b"), (("/a", "b", "c"), "/a/b/c")])
def test_join_path_strs(strs, expected):
    assert join_path_strs(*strs) == expected
