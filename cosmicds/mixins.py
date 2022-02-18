from ipyvuetify import VuetifyTemplate
from glue.core import HubListener

__all__ = ['HubMixin', 'TemplateMixin']


class HubMixin(HubListener):
    @property
    def app(self):
        return self._session.application

    @property
    def hub(self):
        return self._session.hub

    @property
    def session(self):
        return self._session

    @property
    def data_collection(self):
        return self._session.data_collection


class TemplateMixin(VuetifyTemplate, HubMixin):
    pass