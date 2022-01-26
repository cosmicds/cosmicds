import ipyvue as v

from astropy.coordinates import Angle
import astropy.units as u
from cosmicds.utils import RepeatedTimer, load_template
from datetime import datetime
from ipywidgets import DOMWidget, widget_serialization
from traitlets import Bool, Instance, Int

class GalaxySelectionTool(v.VueTemplate):
    template = load_template("galaxy_selection_tool.vue", __file__).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)
    pan_count = Int(0).tag(sync=True)
    zoom_count = Int(0).tag(sync=True)
    exploration_complete = Bool(False).tag(sync=True)
    _fov = Angle(0 * u.deg)
    _ra = Angle(0 * u.deg)
    _dec = Angle(0 * u.deg)
    _panning = False
    _zooming = False

    UPDATE_TIME = 1 #seconds

    def __init__(self, wwt, *args, **kwargs):
        self.widget = wwt
        self.widget._set_message_type_callback('wwt_view_state', self._handle_view_message)
        self.last_update = datetime.now()
        self._rt = RepeatedTimer(self.UPDATE_TIME, self._update_if_needed)
        super().__init__(*args, **kwargs)

    def _update_if_needed(self):
        delta = datetime.now() - self.last_update
        if delta.total_seconds() >= self.UPDATE_TIME:
            self._update_zooming(False)
            self._update_panning(False)


    def _update_zooming(self, zooming):
        if not zooming and self._zooming:
            self.zoom_count += 1
        self._zooming = zooming

    def _update_panning(self, panning):
        if not panning and self._panning:
            self.pan_count += 1
        self._panning = panning

    def _handle_view_message(self, _wwt, _updated):
        fov = Angle(self.widget.get_fov())
        center = self.widget.get_center()
        ra = Angle(center.ra)
        dec = Angle(center.dec)
        zooming = not u.isclose(fov, self._fov)
        panning = not u.allclose([ra, dec], [self._ra, self._dec])
        self._update_panning(panning)
        self._update_zooming(zooming)
        self._ra = ra
        self._dec = dec
        self._fov = fov
        self.last_update = datetime.now()
        if self.pan_count >= 3 and self.zoom_count >= 3:
            self.exploration_complete = True
            self.widget._set_message_type_callback('wwt_view_state', None)


