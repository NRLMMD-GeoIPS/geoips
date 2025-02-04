# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""
The Geolocated Information Processing System (GeoIPS).

GeoIPS |unireg| Base Package
----------------------------

The GeoIPS Base Package provides a Python 3 based architecture supporting a wide
variety of satellite and weather data processing. The modular nature of the GeoIPS
base infrastructure also allows plug-and-play capability for user-specified custom
functionality.

Homepage: https://github.com/NRLMMD-GEOIPS/geoips

.. |unireg|    unicode:: U+000AE .. REGISTERED SIGN
"""

from geoips import errors
from geoips import filenames
from geoips import interfaces
from geoips import utils
from geoips import xarray_utils
from ._version import __version__, __version_tuple__

import logging  # noqa
from geoips.commandline.log_setup import add_logging_level

from matplotlib import rcParams

# Disable interpolation in calls to matplotlib.plt.imshow()
# Interpolation will still work for other plotting functions.
# This is disabled because we pre-interpolate our imagery and
# we don't need matplotlib to reinterpolate. We explicitly compute
# the size our our axes instances to accommodate the imagery.
rcParams["image.interpolation"] = "none"


add_logging_level("INTERACTIVE", 35)

__all__ = [
    "interfaces",
    "errors",
    "filenames",
    "utils",
    "xarray_utils",
    "__version__",
    "__version_tuple__",
]
