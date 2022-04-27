from glue_jupyter.bqplot.scatter import BqplotScatterView
from cosmicds.viewers import cds_viewer

__all__ = ["HubbleFitView", "HubbleScatterView"]

HubbleFitView = cds_viewer(BqplotScatterView, [
    "bqplot:home",
    "bqplot:rectzoom",
    "bqplot:rectangle",
    "cds:linedraw",
    "cds:linefit"
],
'Fit View')

HubbleScatterView = cds_viewer(BqplotScatterView, [
    'bqplot:home',
    'bqplot:rectzoom',
    'bqplot:rectangle',
    'cds:linefit'
],
'Scatter View')
