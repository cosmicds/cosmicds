# This file is for viewers that don't need anything beyond
# the standard CDS updating (the new toolbar, etc.)
from glue_plotly.viewers.histogram import PlotlyHistogramView
from glue_plotly.viewers.scatter import PlotlyScatterView

from numpy import spacing

from .state import CDSHistogramViewerState, CDSScatterViewerState
from .viewer import cds_viewer

from .dotplot import PlotlyDotPlotView

CDSScatterView = cds_viewer(
    PlotlyScatterView,
    state_cls=CDSScatterViewerState,
    name='CDSScatterView',
    viewer_tools=[
        'plotly:home',
        'plotly:zoom',
    ],
    label='2D scatter'
)

CDSHistogramView = cds_viewer(
    PlotlyHistogramView,
    state_cls=CDSHistogramViewerState,
    name='CDSHistogramView',
    viewer_tools=[
        'plotly:home',
        'plotly:hzoom',
    ],
    label='Histogram'
)

CDSDotPlotView = cds_viewer(
    PlotlyDotPlotView,
    state_cls=CDSHistogramViewerState,
    name='CDSDotPlotView',
    viewer_tools=[
        'plotly:home'
    ],
    label="Dot Plot"
)
