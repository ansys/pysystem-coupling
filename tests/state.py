class StateForTesting:
    def __init__(self):
        self.__state = {}

    def set_state(self, path, state):
        comps = _split_comps(path)
        if not comps:
            raise Exception("Path is empty")

        last = comps.pop()
        s = self.__state
        for comp in comps:
            s = s.setdefault(comp, {})
        if last in s:
            new_state = s[last]
            for k, v in state.items():
                new_state[k] = v
            s[last] = new_state
        else:
            s[last] = state
        import pprint

        print(f"set {path} state to\n{pprint.pformat(self.__state)}")

    def get_state(self, path):
        print(f"get_state(path={path})")
        comps = _split_comps(path)

        s = self.__state
        found_some = False
        for comp in comps:
            if comp in s:
                found_some = True
                s = s[comp]
            else:
                return {}
        if found_some:
            print(f"get_state: {s}")
        return s if found_some else {}

    def get_parameter(self, path, name):
        s = self.get_state(path)
        return s.get(name, None)

    def delete_object(self, path):
        comps = _split_comps(path)
        if not comps:
            raise Exception("Path is empty")
        last = comps.pop()
        s = self.__state
        found = False
        for comp in comps:
            if comp in s:
                found = True
                s = s[comp]
            else:
                found = False
                break
        if found and last in s:
            del s[last]

    def create(self, path, name):
        self.set_state(path + "/" + name, {})


def _split_comps(path):
    comps = path.split("/")
    if comps:
        ret = []
        if comps[0] == "":
            comps = comps[1:]
        for c in comps:
            if ":" in c:
                t, _, n = c.partition(":")
                ret.extend((t, n))
            else:
                ret.append(c)
        comps = ret
    return comps
