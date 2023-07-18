# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView

from numpy import spacing

from .state import CDSHistogramViewerState, CDSScatterViewerState
from .viewer import cds_viewer

CDSScatterView = cds_viewer(
    BqplotScatterView,
    state_cls=CDSScatterViewerState,
    name='CDSScatterView',
    viewer_tools=[
        'bqplot:home',
        'bqplot:rectzoom',
        'bqplot:rectangle'
    ],
    label='2D scatter'
)

CDSHistogramView = cds_viewer(
    BqplotHistogramView,
    state_cls=CDSHistogramViewerState,
    name='CDSHistogramView',
    viewer_tools=[
        'bqplot:home',
        'bqplot:xzoom',
        'bqplot:xrange'
    ],
    label='Histogram'
)
