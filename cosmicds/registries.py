from glue.config import DictRegistry
from ipyvuetify import VuetifyTemplate
from ipywidgets import Widget

__all__ = ['stage_registry']


class UniqueDictRegistry(DictRegistry):
    """
    Base registry class that handles hashmap-like associations between a string
    representation of a plugin and the class to be instantiated.
    """
    def add(self, name, step, cls):
        """
        Add an item to the registry.
        Parameters
        ----------
        name : str
            The name referencing the associated class in the registry.
        cls : type
            The class definition (not instance) associated with the name given
            in the first parameter.
        """
        self.members.setdefault(name, {})[step] = cls


class StageRegistry(UniqueDictRegistry):
    """
    Registry containing references to plugins which will populate the
    application-level toolbar.
    """
    def __call__(self, name, step):
        def decorator(cls):
            # The class must inherit from `Widget` in order to be
            # ingestible by the component initialization.
            if not issubclass(cls, VuetifyTemplate):
                raise ValueError(
                    f"Unrecognized superclass for `{cls.__name__}`. All "
                    f"registered tools must inherit from "
                    f"`ipyvuetify.VuetifyTemplate`.")

            self.add(name, step, cls)
            return cls
        return decorator


stage_registry = StageRegistry()
