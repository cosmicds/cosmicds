from cosmicds.registries import stage_registry
from cosmicds.utils import load_template
from ipyvuetify import VuetifyTemplate
from glue.core import HubListener


@stage_registry(name="hubbles_law", step=1)
class StageOne(VuetifyTemplate, HubListener):
    template = load_template("stage_one.vue", __file__).tag(sync=True)

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = session
