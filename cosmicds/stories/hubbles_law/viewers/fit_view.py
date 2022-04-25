from glue_jupyter.bqplot.scatter import BqplotScatterView
from cosmicds.viewers import cds_viewer

CDSFitView = cds_viewer(BqplotScatterView, [
    "bqplot:home",
    "bqplot:rectzoom",
    "bqplot:rectangle",
    "cds:linedraw",
    "cds:linefit"
],
'Fit View')
