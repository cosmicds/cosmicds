# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)
from glue_jupyter.bqplot.scatter import BqplotScatterView
from glue_jupyter.bqplot.histogram import BqplotHistogramView

from .state import CDSScatterState
from .viewer import cds_viewer

CDSScatterView = cds_viewer(
    BqplotScatterView,
    state_cls=CDSScatterState,
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
    name='CDSHistogramView',
    viewer_tools=[
        'bqplot:home',
        'bqplot:xzoom',
        'bqplot:xrange'
    ],
    label='Histogram'
)
