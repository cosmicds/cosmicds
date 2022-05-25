from astropy import units as u
from bqplot.scales import LinearScale
from bqplot_image_gl import LinesGL
from glue_jupyter.bqplot.histogram.layer_artist import BqplotHistogramLayerArtist
from glue_jupyter.bqplot.scatter.layer_artist import BqplotScatterLayerArtist

try:
    from astropy.cosmology import Planck18 as planck
except ImportError:
    from astropy.cosmology import Planck15 as planck

__all__ = [
    'HUBBLE_ROUTE_PATH',
    'MILKY_WAY_SIZE_MPC', 'H_ALPHA_REST_LAMBDA',
    'MG_REST_LAMBDA', 'GALAXY_FOV', 'FULL_FOV',
    'angle_to_json', 'angle_from_json',
    'age_in_gyr', 'format_fov', 'format_measured_angle',
    'line_mark', 'vertical_line_mark',
]

HUBBLE_ROUTE_PATH = "hubbles_law"

MILKY_WAY_SIZE_MPC = 0.03

# Both in angstroms
H_ALPHA_REST_LAMBDA = 6565 # SDSS calibrates to wavelengths in a vacuum
MG_REST_LAMBDA = 5172 # The value used by SDSS is actually 5176.7, but that wavelength aligns with an upward bump, so we are adjusting it to 5172 to avoid confusing students. Ziegler & Bender 1997 uses lambda_0 ~ 5170, so our choice is justifiable.

GALAXY_FOV = 1.5 * u.arcmin
FULL_FOV = 60 * u.deg

def angle_to_json(angle, _widget):
    return {
        "value": angle.value,
        "unit": angle.unit.name
    }

def angle_from_json(jsn, _widget):
    return jsn["value"] * u.Unit(jsn["unit"])

def age_in_gyr(H0):
    """
    Given a value for the Hubble constant, computes the age of the universe
    in Gyr, based on the Planck cosmology.

    Parameters
    ----------
    H0: float
        The value of the Hubble constant

    Returns
    ----------
    age: numpy.float64
        The age of the universe, in Gyr
    """
    age = planck.clone(H0=H0).age(0)
    unit = age.unit
    return age.value * unit.to(u.Gyr)


def format_fov(fov):
    return fov.to_string(unit=u.degree, sep=":", precision=0, pad=True) + " (dd:mm:ss)"

def format_measured_angle(angle):
    if angle == 0:
        return ""
    return angle.to_string(unit=u.arcsec, precision=0)[:-6] + " arcseconds"

def line_mark(layer, start_x, start_y, end_x, end_y, color, label=None):
    """
    Creates a LinesGL mark between the given start and end points
    using the scales of the given layer.

    Parameters
    ----------
    layer : `glue.viewers.common.layer_artist.LayerArtist`
        The layer used to determine the line's scales.
    start_x : int or float
        The x-coordinate of the line's starting point.
    start_y : int or float
        The y-coordinate of the line's starting point.
    end_x : int or float
        The x-coordinate of the line's endpoint.
    end_y : int or float
        The y-coordinate of the line's endpoint.
    color : str
        The desired color of the line, represented as a hex string.
    """
    if isinstance(layer, BqplotScatterLayerArtist):
        scales = layer.image.scales
    elif isinstance(layer, BqplotHistogramLayerArtist):
        layer_scales = layer.view.scales
        layer_x = layer_scales['x']
        layer_y = layer_scales['y']
        scales = {
            'x': LinearScale(min=layer_x.min, max=layer_x.max, allow_padding=layer_x.allow_padding),
            'y': LinearScale(min=layer_y.min, max=layer_y.max, allow_padding=layer_y.allow_padding),
        }
    return LinesGL(x=[start_x, end_x],
                   y=[start_y, end_y],
                   scales=scales,
                   colors=[color],
                   labels=[label] if label is not None else [],
                   display_legend=label is not None,
                   labels_visibility='label')

def vertical_line_mark(layer, x, color, label=None):
    """
    A specialization of `line_mark` specifically for vertical lines.

    Parameters
    ----------
    layer : `glue.viewers.common.layer_artist.LayerArtist`
        The layer used to determine the line's scales.
    x : int or float
        The x-coordinate of the vertical line
    color : str
        The desired color of the line, represented as a hex string.
    """
    viewer_state = layer.state.viewer_state
    return line_mark(layer, x, viewer_state.y_min, x, viewer_state.y_max, color, label)
