from typing import Iterable, List


def to_typelist(path: str) -> List[str]:
    """Return types in path (meaning discarding names) as a list."""
    if "/" not in path:
        return []
    if ":" not in path:
        return path.split("/")[1:]
    return [c.split(":")[0] for c in path.split("/")][1:]


def to_typepath(path: str) -> str:
    """Return path as a type path (meaning a path of types)."""
    if ":" not in path:
        return path
    return "/".join(c.split(":")[0] for c in path.split("/"))


def join_path_strs(*path_strs: Iterable[str]) -> str:
    """Join a list of strings as a path string.

    .. note::
       A leading empty path component is required for a
       leading path separtator (``/``) in the returned value.
    """
    return "/".join(path_strs)
