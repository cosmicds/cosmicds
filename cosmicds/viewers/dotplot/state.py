from echo.core import add_callback, delay_callback, CallbackProperty
from glue.viewers.histogram.state import HistogramLayerState, HistogramViewerState


class DotPlotViewerState(HistogramViewerState):

    viewer_height = CallbackProperty(400) # in pixels

    def __init__(self, **kwargs):
        super(DotPlotViewerState, self).__init__(**kwargs)
        add_callback(self, 'x_min', self._update_bins)
        add_callback(self, 'x_max', self._update_bins)

    def _update_bins(self, arg=None):
        with delay_callback(self, 'hist_x_min', 'hist_x_max'):
            self.hist_x_min = self.x_min
            self.hist_x_max = self.x_max


class DotPlotLayerState(HistogramLayerState):

    rotation = CallbackProperty(0)
    skew = CallbackProperty(0)

    def __init__(self, **kwargs):
        super(DotPlotLayerState, self).__init__(**kwargs)
