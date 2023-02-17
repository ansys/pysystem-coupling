from abc import ABC, abstractmethod


class SycProxyInterface(ABC):  # pragma: no cover
    """Provides an abstract base class defining the interface for the SystemCoupling
    *proxy* object that the ``datamodel` module depends on.

    While Python doesn't strictly need this class, it is a
    significant testing seam and is useful to make explicit the
    interface depended on.
    """

    @abstractmethod
    def get_static_info(self, category):
        pass

    @abstractmethod
    def get_version(self):
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
    def get_property_options(self, path, name):
        pass

    @abstractmethod
    def execute_cmd(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute_injected_cmd(self, *args, **kwargs):
        pass
