from glue_jupyter.state_traitlets_helpers import GlueState
from traitlets.utils.bunch import Bunch

class CDSGlueState(GlueState):

    def on_state_change(self, *args, obj=None, **kwargs):
        if self._block_on_state_change:
            return
        obj.notify_change(Bunch({'name': self.name,
                                 'type': 'change',
                                 'value': self.get(obj),
                                 'new': self.get(obj)}))
