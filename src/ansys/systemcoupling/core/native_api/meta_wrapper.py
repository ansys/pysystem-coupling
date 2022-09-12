class MetaWrapper:
    def __init__(self, dm_meta, cmd_meta):
        self.__dm_meta = dm_meta
        self.__cmd_meta = cmd_meta

    def __getattr__(self, name):
        try:
            return getattr(self.__dm_meta, name)
        except AttributeError:
            return getattr(self.__cmd_meta, name)
