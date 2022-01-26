def to_typelist(path):
    if '/' not in path:
        return []
    if ':' not in path:
        return path.split('/')[1:]
    return [c.split(':')[0] for c in path.split('/')][1:]

def to_typepath(path):
    if ':' not in path:
        return path
    return '/'.join(c.split(':')[0] for c in path.split('/'))

def join_path_strs(*path_strs):
    return '/'.join(path_strs)
