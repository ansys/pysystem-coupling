class CommandMetadata:
    def __init__(self, raw_data):
        self._init_data(raw_data)
    
    def _init_data(self, raw_data):
        self.__data = {item['name']: item for item in raw_data}
    
    def get_object_path_command_and_query_names(self):
        return list(self.__data.keys())
       
    def is_command_or_query(self, name):
        return name in self.__data

    def is_object_path_command_or_query(self, name):
        info = self.__data.get(name, None)
        return info and 'ObjectPath' in info['args']
