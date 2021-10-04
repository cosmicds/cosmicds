from glue.core.hub import Hub
import numpy as np
from glue.core.message import (DataCollectionAddMessage,
                               DataCollectionDeleteMessage)
from glue.core import HubListener
from ipyvuetify import VuetifyTemplate
from traitlets import Bool, List, Unicode

from ...utils import load_template

__all__ = ['Table']


class Table(VuetifyTemplate, HubListener):
    template = load_template("table.vue", __file__).tag(sync=True)
    headers = List([
        {
            'text': 'Student ID',
            'value': 'student_id',
            'align': 'start'
        },
        {
            'text': 'Distance',
            'value': 'distance'
        },
        {
            'text': 'Velocity',
            'value': 'velocity'
        },
        {
            'text': 'Type',
            'value': 'type'
        }]).tag(sync=True)
    items = List().tag(sync=True)
    search = Unicode().tag(sync=True)
    single_select = Bool(False).tag(sync=True)
    selected = List().tag(sync=True)

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = session
        self._subset_group = None

        # Populate the table with the current data in the collection
        self._on_data_collection_updated()

        # Subscribe to change events that alter the data collection so that
        # the table can be updated accordingly
        self.hub.subscribe(self, DataCollectionAddMessage,
                           handler=self._on_data_collection_updated)
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_updated)

        # Listen for changes to selected rows
        self.observe(self.on_selected_changed, names=['selected'])

    @property
    def data_collection(self):
        return self._session.data_collection

    @property
    def hub(self):
        return self._session.hub

    def _on_data_collection_updated(self):
        df = self.data_collection['random_data0'].to_dataframe()
        self.items = [
            {
                'student_id': row.student_id,
                'distance': row.distance,
                'velocity': row.velocity,
                'type': row.galaxy_type
            } for row in df.itertuples()
        ]

    def on_selected_changed(self, event):
        student_ids = [x['student_id'] for x in event['new']]
        data = self.data_collection['random_data0']
        state = np.bitwise_or.reduce([data.id['student_id'] == x for x in student_ids])

        # Remove previous subset group
        self.data_collection.remove_subset_group(self._subset_group)

        # Add new subset group
        self._subset_group = self.data_collection.new_subset_group("selected", state)
        self._subset_group.style.color = '#00ff00'
