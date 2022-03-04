from glue.config import DictRegistry
from ipyvuetify import VuetifyTemplate
from ipywidgets import Widget
from glue.core.state_objects import State
import warnings

__all__ = ['stage_registry']


class UniqueDictRegistry(DictRegistry):
    """
    Base registry class that handles hashmap-like associations between a string
    representation of a plugin and the class to be instantiated.
    """
    def add(self, name, cls):
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
        self.members[name] = cls


class StoryRegistry(UniqueDictRegistry):
    """
    Registry containing references to plugins which will populate the
    application-level toolbar.
    """
    def __init__(self):
        super().__init__()

        self._instance_db = []

    def __call__(self, name):
        def decorator(cls):
            # The class must inherit from `Widget` in order to be
            # ingested by the component initialization.
            if not issubclass(cls, State):
                raise ValueError(
                    f"Unrecognized superclass for `{cls.__name__}`. All "
                    f"registered tools must inherit from "
                    f"`ipyvuetify.VuetifyTemplate`.")

            self.add(name, cls)
            return cls
        return decorator

    def setup_story(self, name, session):
        if name not in self.members:
            raise ValueError(f"Story `{name}` does not exist in the "
                             "registery.")

        story_entry = self.members[name]
        story_state = story_entry['cls'](session)
        story_state.name = name

        for k, v in story_entry['stages'].items():
            stage = v['cls'](session, story_state)
            
            story_state.stages[k] = {"title": stage.title,
                                     "subtitle": stage.subtitle,
                                     "step_index": 0,
                                     "steps": [{'title': x, 'completed': False} 
                                               for x in v['steps']],
                                     "model_id": f"IPY_MODEL_{stage.model_id}",
                                     "_instance": stage}

        return story_state

    def register_stage(self, story, index, steps):
        def decorator(cls):
            # The class must inherit from `Widget` in order to be
            # ingested by the component initialization.
            if not issubclass(cls, VuetifyTemplate):
                raise ValueError(
                    f"Unrecognized superclass for `{cls.__name__}`. All "
                    f"registered tools must inherit from "
                    f"`ipyvuetify.VuetifyTemplate`.")

            # Check to see if the given story has been registered
            if not story in self.members:
                raise ValueError(f"Story `{story}` does not exist in the "
                                 "registery.")

            self.members[story]['stages'][index] = {'cls': cls, 'steps': steps}
            return cls
        return decorator

    def add(self, name, cls):
        self.members[name] = {'cls': cls, 'stages': {}}



class StageRegistry(UniqueDictRegistry):
    """
    Registry containing references to plugins which will populate the
    application-level toolbar.
    """
    def __call__(self, name, index):
        def decorator(cls):
            # The class must inherit from `Widget` in order to be
            # ingestible by the component initialization.
            if not issubclass(cls, VuetifyTemplate):
                raise ValueError(
                    f"Unrecognized superclass for `{cls.__name__}`. All "
                    f"registered tools must inherit from "
                    f"`ipyvuetify.VuetifyTemplate`.")

            self.add(name, index, cls)
            return cls
        return decorator

    def add(self, name, index, cls):
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
        self.members.setdefault(name, {})[index] = cls


stage_registry = StageRegistry()
story_registry = StoryRegistry()
register_stage = story_registry.register_stage
