from math import floor, pi

from echo.core import add_callback
from glue.utils import color2hex
from glue_jupyter.bqplot.histogram.layer_artist import BqplotHistogramLayerArtist
from glue_jupyter.link import dlink, link

from bqplot import Scatter, ScatterGL, LinearScale
from numpy import inf

from cosmicds.viewers.dotplot.state import DotPlotLayerState


class BqplotDotPlotLayerArtist(BqplotHistogramLayerArtist):

    _layer_state_cls = DotPlotLayerState

    def __init__(self, view, viewer_state, layer_state=None, layer=None):

        super(BqplotHistogramLayerArtist, self).__init__(viewer_state,
                                                         layer_state=layer_state, layer=layer)

        self.view = view

        self.scales = {
            **self.view.scales,
            'rotation': LinearScale(min=0, max=180)
        }
        self.bars = Scatter(scales=self.scales,
                            x=[0, 1],
                            y=[0, 1],
                            marker='ellipse')

        self.view.figure.marks = list(self.view.figure.marks) + [self.bars]

        dlink((self.state, 'color'), (self.bars, 'colors'), lambda x: [color2hex(x)])
        dlink((self.state, 'alpha'), (self.bars, 'opacities'), lambda x: [x])
        dlink((self.state, 'skew'), (self.bars, 'default_skew'))

        self._viewer_state.add_global_callback(self._update_histogram)
        self.state.add_global_callback(self._update_histogram)
        self.bins = None

        link((self.state, 'visible'), (self.bars, 'visible'))

        # Because of how the glue_jupyter link class checks for updates, we currently can't
        # do this as a link or dlink - the equality check in there doesn't correctly handle
        # numpy arrays of size > 1
        add_callback(self.state, 'rotation', self._update_rotation)

        add_callback(self._viewer_state, 'x_min', self._update_size)
        add_callback(self._viewer_state, 'x_max', self._update_size)
        add_callback(self._viewer_state, 'viewer_height', self._update_size)

    def _update_size(self, arg=None):
        if self._viewer_state.y_max is not None and self._viewer_state.y_min is not None:
            y_range = max(self._viewer_state.y_max - self._viewer_state.y_min, 1)
            if y_range == 0:
                self._viewer_state.y_max += 1
                y_range = 1

            # The default_size parameter in bqplot specifies the area of the mark in pixels
            # but we know what pixel height (i.e. diameter) we want
            # so the size should be (pi / 4) * height ^ 2
            pixel_height = (self._viewer_state.viewer_height + self.view.figure.fig_margin["top"]) / y_range


            # Shrink and scale height to add a bit of space
            spacing = 1
            scaling = 0.7
            size = floor((pi / 4) * ((scaling * pixel_height - spacing) ** 2))
            size = max(size, 1)
            self.bars.default_size = size

    def _scale_histogram(self):
        # TODO: comes from glue/viewers/histogram/layer_artist.py
        if self.bins is None:
            return  # can happen when the subset is empty

        if self.bins.size == 0:
            return

        self.hist = self.hist_unscaled.astype(float)
        dx = self.bins[1] - self.bins[0]

        if self._viewer_state.cumulative:
            self.hist = self.hist.cumsum()
            if self._viewer_state.normalize:
                self.hist /= self.hist.max()
        elif self._viewer_state.normalize:
            self.hist /= (self.hist.sum() * dx)

        # TODO this won't work for log ...
        centers = (self.bins[:-1] + self.bins[1:]) / 2
        assert len(centers) == len(self.hist)

        x, y = [], []
        counts = self.hist.astype(int)
        for i in range(self.bins.size - 1):
            x_i = (self.bins[i] + self.bins[i+1])/2
            y_i = range(1, counts[i] + 1)
            x.extend([x_i] * counts[i])
            y.extend(y_i)
     
        self.bars.x = x
        self.bars.y = y
        self._update_size()

        # We have to do the following to make sure that we reset the y_max as
        # needed. We can't simply reset based on the maximum for this layer
        # because other layers might have other values, and we also can't do:
        #
        #   self._viewer_state.y_max = max(self._viewer_state.y_max, result[0].max())
        #
        # because this would never allow y_max to get smaller.

        self.state._y_max = self.hist.max()
        if self._viewer_state.y_log:
            self.state._y_max *= 2
        else:
            self.state._y_max *= 1.2

        if self._viewer_state.y_log:
            self.state._y_min = self.hist[self.hist > 0].min() / 10
        else:
            self.state._y_min = 0

        largest_y_max = max((getattr(layer, '_y_max', 0)
                            for layer in self._viewer_state.layers if layer.visible), default = self.state._y_max)
        if largest_y_max != self._viewer_state.y_max:
            self._viewer_state.y_max = largest_y_max

        smallest_y_min = min((getattr(layer, '_y_min', inf)
                             for layer in self._viewer_state.layers if layer.visible), default = self.state._y_min)
        if smallest_y_min != self._viewer_state.y_min:
            self._viewer_state.y_min = smallest_y_min

        self.redraw()

    def _update_rotation(self, rotation):
        self.bars.rotation = [rotation] * len(self.bars.x)
