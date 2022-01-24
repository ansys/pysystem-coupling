class StateForTesting:
    def __init__(self):
        self.__state = {}
    
    def set_state(self, path, state):
        comps = path.split('/')
        if comps and comps[0] == '':
            comps = comps[1:]
        if not comps:
            raise Exception('Path is empty')

        comps, last = comps[:-1], comps[-1]
        s = self.__state
        for comp in comps:
            s = s.setdefault(comp, {})
        s[last] = state
    
    def get_state(self, path):
        comps = path.split('/')
        if comps and comps[0] == '':
            comps = comps[1:]

        s = self.__state
        found_some = False
        for comp in comps:
            if comp in s:
                found_some = True
                s = s[comp]
            else:
                return {}
            
        return s if found_some else {}
   
    def get_parameter(self, path, name):
        s = self.get_state(path)
        return s.get(name, None)
    