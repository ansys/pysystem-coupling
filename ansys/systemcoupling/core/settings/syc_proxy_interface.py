from abc import ABC, abstractmethod


class SycProxyInterface(ABC):
    """Abstract base defining the interface for the SystemCoupling
    'proxy' object that the `datamodel` module depends on.

    As this is Python, we don't strictly need this, but it is a
    significant testing seam and it is useful to make explicit the
    interface depended on.
    """

    @abstractmethod
    def get_static_info(self):
        pass

    @abstractmethod
    def set_state(self, path, state):
        pass

    @abstractmethod
    def get_state(self, path):
        pass

    @abstractmethod
    def delete(self, path):
        pass

    @abstractmethod
    def create_named_object(self, path, name):
        pass

    @abstractmethod
    def get_object_names(self, path):
        pass

    @abstractmethod
    def execute_cmd(self, *args, **kwargs):
        pass
