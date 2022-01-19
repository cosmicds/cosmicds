from ipyvuetify import VuetifyTemplate
from glue.core import HubListener

__all__ = ['TemplateMixin']


class TemplateMixin(VuetifyTemplate, HubListener):
    @property
    def hub(self):
        return self._app.session.hub

    @property
    def session(self):
        return self._app.session

    @property
    def data_collection(self):
        return self._app.session.data_collection