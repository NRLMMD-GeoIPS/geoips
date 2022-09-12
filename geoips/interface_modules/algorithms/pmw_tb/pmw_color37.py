# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # # 
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # # 
# # # This program is free software:
# # # you can redistribute it and/or modify it under the terms
# # # of the NRLMMD License included with this program.
# # # 
# # # If you did not receive the license, see
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/
# # # for more information.
# # # 
# # # This program is distributed WITHOUT ANY WARRANTY;
# # # without even the implied warranty of MERCHANTABILITY
# # # or FITNESS FOR A PARTICULAR PURPOSE.
# # # See the included license for more details.

''' Data manipulation steps for "color37" product.

    This algorithm expects Brightness Temperatures in units of degrees Kelvin
'''

import logging

LOG = logging.getLogger(__name__)

family = 'list_numpy_to_numpy'
alg_func_type = 'list_numpy_to_numpy'
description = 'Passive Microwave 37 MHz Colorized Brightness Temperature'


def pmw_color37(arrays):
    ''' Data manipulation steps for "color37" product algorithm.

    This algorithm expects Brightness Temperatures in units of degrees Kelvin,
    and returns red green and blue gun arrays.

    Args:
        data (list[numpy.ndarray]) : 
            * list of numpy.ndarray or numpy.MaskedArray of channel data, in order of channels list above
            * Degrees Kelvin

    Returns:
        numpy.ndarray : numpy.ndarray or numpy.MaskedArray of qualitative RGBA image output
    '''

    h37 = arrays[0]
    v37 = arrays[1]

    from geoips.data_manipulations.corrections import apply_data_range, apply_gamma
    red = 2.181*v37 - 1.181*h37
    red = apply_data_range(red, 260.0, 280.0,
                           min_outbounds='crop', max_outbounds='crop',
                           norm=True, inverse=True)
    red = apply_gamma(red, 1.0)

    grn = (v37 - 180.0) / (300.0 - 180.0)
    grn = apply_data_range(grn, 0.0, 1.0,
                           min_outbounds='crop', max_outbounds='crop',
                           norm=True, inverse=False)
    grn = apply_gamma(grn, 1.0)

    blu = (h37 - 160.0) / (300.0 - 160.0)
    blu = apply_data_range(blu, 0.0, 1.0,
                           min_outbounds='crop', max_outbounds='crop',
                           norm=True, inverse=False)
    blu = apply_gamma(blu, 1.0)

    from geoips.image_utils.mpl_utils import alpha_from_masked_arrays, rgba_from_arrays
    alp = alpha_from_masked_arrays([red, grn, blu])
    rgba = rgba_from_arrays(red, grn, blu, alp)
    return rgba
