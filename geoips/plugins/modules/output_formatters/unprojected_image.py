# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Matplotlib-based unprojected image output."""

import logging
from os.path import basename, dirname, join

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from geoips.image_utils.mpl_utils import save_image

matplotlib.use("agg")

LOG = logging.getLogger(__name__)

interface = "output_formatters"
family = "unprojected"
name = "unprojected_image"


def call(
    xarray_obj,
    product_name,
    output_fnames,
    product_name_title=None,
    mpl_colors_info=None,
    x_size=None,
    y_size=None,
    savefig_kwargs=None,
    is_3d=False,
):
    """Plot unprojected image to matplotlib figure."""
    if savefig_kwargs is None:
        # Default to no arguments, empty dictionary.  Will result in masked background
        savefig_kwargs = {}
        # black background
        # savefig_kwargs = {'facecolor': 'k'}

    if product_name_title is None:
        product_name_title = product_name
    if x_size is None and y_size is None:
        x_size = xarray_obj[product_name].shape[1]
        y_size = xarray_obj[product_name].shape[0]
    elif y_size is None:
        ratio = float(x_size) / float(xarray_obj[product_name].shape[1])
        y_size = float(ratio) * float(xarray_obj[product_name].shape[0])
    elif x_size is None:
        ratio = float(y_size) / float(xarray_obj[product_name].shape[0])
        x_size = float(ratio) * float(xarray_obj[product_name].shape[1])

    rc_params = matplotlib.rcParams
    dpi = rc_params["figure.dpi"]

    image_width = float(x_size) / dpi
    image_height = float(y_size) / dpi

    fig = plt.figure(facecolor="none")
    fig.set_size_inches(image_width, image_height)
    main_ax = plt.Axes(fig, [0, 0, 1, 1])
    main_ax.set_axis_off()
    fig.add_axes(main_ax)

    if is_3d:
        slices = [
            xarray_obj[product_name].data[slice]
            for slice in range(xarray_obj[product_name].data.shape[0])
        ]
    else:
        slices = [xarray_obj[product_name].data]
    for slice_idx, slice_data in enumerate(slices):
        main_ax.clear()
        # Needs to be flipped upside-down as incoming data is flipped if unprojected.
        # This is the case for family
        # unsectored_xarray_dict_to_algorithm_to_output_format, but I'm not sure if it
        # applies to all other families that use this output formatter. We should look
        # into this.
        main_ax.imshow(
            np.flipud(slice_data),
            norm=mpl_colors_info["norm"],
            cmap=mpl_colors_info["cmap"],
        )

        success_outputs = []
        for fname in output_fnames:
            if is_3d:
                # This is generic for overcast data, on the order of (level) * 0.5 km.
                # I.e. if level == 5, lvl_str == '02_50.'. This is an easy way to denote
                # what height each image corresponds to, though I'm not sure if we
                # should hardcode this string here. Maybe create a new filename
                # formatter for that data or we can add a new argument to this plugin
                # which handles fname conventions for 3D data. Such as a function which
                # produces a pre-prended string to the corresponding fname.
                lvl_km = str(slice_idx * 0.5).split(".")
                lvl_str = f"{lvl_km[0].zfill(2)}_{lvl_km[1]}0."
                final_fname = join(dirname(fname), f"{lvl_str}{basename(fname)}")
            else:
                final_fname = fname
            LOG.info("Plotting %s with plt", fname)
            # This just handles cleaning up the axes, creating directories, etc
            success_outputs += save_image(
                fig,
                final_fname,
                is_final=False,
                image_datetime=xarray_obj.start_datetime,
                savefig_kwargs=savefig_kwargs,
            )

    return success_outputs
