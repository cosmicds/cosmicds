from glue.config import DictRegistry
from ipyvuetify import VuetifyTemplate
from glue.core.state_objects import State
import requests

from cosmicds.utils import API_URL, request_session, log_to_console

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

    def setup_story(self, name, session, app_state):
        if name not in self.members:
            raise ValueError(f"Story `{name}` does not exist in the "
                             "registry.")

        story_entry = self.members[name]
        story_state = story_entry['cls'](session)
        story_state.name = name

        # This should only get run once per story - using a one-off session is fine for now
        response = request_session().get(f"{API_URL}/story-state/{app_state.student['id']}/{name}")
        data = response.json()
        state = data["state"]

        if state is not None:
            state["stages"] = { int(k) : v for k, v in state["stages"].items() }
            story_state.update_from_dict(state)

        story_state.setup_for_student(app_state)

        for k, v in sorted(story_entry['stages'].items()):
            stage_cls = v['cls']
            stage_state = stage_cls._state_cls()
            log_to_console(f"Setting up stage {k}")
            if state is not None and k in state["stages"] and "state" in state["stages"][k]:
                stage_state.update_from_dict(state["stages"][k]["state"])
            stage = stage_cls(session, story_state, app_state, index=k, stage_state=stage_state)

            stage.stage_state.add_global_callback(story_state.write_to_db)
            
            story_state.stages[k] = {"title": stage.title,
                                     "subtitle": stage.subtitle,
                                     "state": stage.stage_state,
                                     "step_index": 0,
                                     "steps": [{'title': x, 'completed': False} 
                                               for x in v['steps']],
                                     "model_id": f"IPY_MODEL_{stage.model_id}",
                                     "stage_icon": stage.stage_icon}

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
                                 "registry.")

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
