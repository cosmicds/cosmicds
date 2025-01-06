from uuid import uuid4

from echo import add_callback
from glue.config import viewer_tool
from glue_plotly.viewers import PlotlyBaseView

from cosmicds.widgets.toolbar import Toolbar

from .state import cds_viewer_state


def cds_viewer(viewer_class, name, viewer_tools=[], label=None, state_cls=None):

    state_class = state_cls or viewer_class._state_cls
    cds_state_class = cds_viewer_state(state_class)

    class CDSViewer(viewer_class):

        __name__ = name
        __qualname__ = name
        _state_cls = cds_state_class
        inherit_tools = viewer_tools is None
        tools = viewer_tools or viewer_class.tools
        LABEL = label or viewer_class.LABEL

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ignore_conditions = []
            add_callback(self.state, "xtick_values", self._update_xtick_values)
            add_callback(self.state, "ytick_values", self._update_ytick_values)

            if issubclass(viewer_class, PlotlyBaseView):
                add_callback(self.state, "subtitle", self._update_plotly_subtitle)
                self._create_plotly_subtitle(self.state.subtitle)

        def _create_plotly_subtitle(self, text=None):
            self.figure.add_annotation(text=text,
                                       xref="paper", yref="paper",
                                       x=0.5, y=1.2,
                                       showarrow=False)

        def _update_plotly_subtitle(self, text=None):
            subtitle = next(self.figure.select_annotations(), None)
            if subtitle is not None:
                subtitle.update(text=text)

        def initialize_toolbar(self):

            # If viewer_class has its own custom initialize_toolbar, defer to that
            # This will ONLY be called if it's defined in viewer_class
            if 'initialize_toolbar' in viewer_class.__dict__:
                viewer_class.initialize_toolbar(self)
                return
            
            self.toolbar = Toolbar(self)

            for tool_id in self.tools:
                mode_cls = viewer_tool.members[tool_id]
                mode = mode_cls(self)
                self.toolbar.add_tool(mode)

        def ignore(self, condition):
            self.ignore_conditions.append(condition)

        def add_data(self, data, **kwargs):
            if any(condition(data) for condition in self.ignore_conditions):
                return False
            return super().add_data(data, **kwargs)

        def add_subset(self, subset, **kwargs):
            if any(condition(subset) for condition in self.ignore_conditions):
                return False
            return super().add_subset(subset, **kwargs)

        # The argument here can be either a Data or Subset object
        def layer_artist_for_data(self, data):
            return next((a for a in self.layers if a.layer == data), None)

        def _update_xtick_values(self, values):
            self.axis_x.tickmode = "array"
            self.axis_x.tickvals = values
        
        def _update_ytick_values(self, values):
            self.axis_x.tickmode = "array"
            self.axis_y.tickvals = values

    return CDSViewer
