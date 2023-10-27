# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # #
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # #
# # # This program is free software: you can redistribute it and/or modify it under
# # # the terms of the NRLMMD License included with this program. This program is
# # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
# # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
# # # for more details. If you did not receive the license, for more information see:
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

"""Test script for representative product comparisons."""

import subprocess
import logging
from os.path import splitext

LOG = logging.getLogger(__name__)

interface = "output_checkers"
family = "standard"
name = "geotiff"


def get_test_files(output_path):
    """Return a Series of GeoTIFF paths, randomly modified from compare."""
    import rasterio
    import shutil
    from os import makedirs
    from os.path import exists, join
    from importlib.resources import files
    import numpy as np

    savedir = join(output_path, "scratch", "unit_tests", "test_geotiffs")
    if not exists(savedir):
        makedirs(savedir)

    tif_name = "20200405_000000_SH252020_ahi_himawari-8_WV_100kts_100p00_1p0.tif"
    tif_path = str(files("geoips") / "../tests/outputs/ahi.tc.WV.geotiff" / tif_name)
    shutil.copy(tif_path, join(savedir, "compare.tif"))
    # Prepare paths for matched, close_mismatch, and bad_mismatch
    compare_path = join(savedir, "compare.tif")
    matched_path = join(savedir, "matched.tif")
    close_mismatch_path = join(savedir, "close_mismatch.tif")
    bad_mismatch_path = join(savedir, "bad_mismatch.tif")
    # Load the original GeoTIFF file
    with rasterio.open(compare_path) as src:
        compare_data = src.read()
        profile = src.profile

    # Save the original as 'compare'
    with rasterio.open(compare_path, "w", **profile) as dst:
        dst.write(compare_data)

    # Make a 'matched' version (identical to compare)
    with rasterio.open(matched_path, "w", **profile) as dst:
        dst.write(compare_data)

    # Make a 'close_mismatch' version (slightly modified)
    close_mismatch_data = compare_data + np.random.normal(
        scale=0.05, size=compare_data.shape
    )
    with rasterio.open(close_mismatch_path, "w", **profile) as dst:
        dst.write(close_mismatch_data)

    # Make a 'bad_mismatch' version (strongly modified)
    bad_mismatch_data = compare_data + np.random.normal(
        scale=0.25, size=compare_data.shape
    )
    with rasterio.open(bad_mismatch_path, "w", **profile) as dst:
        dst.write(bad_mismatch_data)

    return compare_path, [matched_path, close_mismatch_path, bad_mismatch_path]


def perform_test_comparisons(plugin, compare_path, output_paths):
    """Test the comparison of two GeoTIFF files with the GeoTIFF Output Checker."""
    from os import remove

    for path_idx in range(len(output_paths)):
        retval = plugin.module.outputs_match(
            plugin,
            output_paths[path_idx],
            compare_path,
        )
        if path_idx == 0:
            assert retval is True
        else:
            assert retval is False
    for path in output_paths:
        remove(path)


def correct_file_format(fname):
    """Determine if fname is a geotiff file.

    Parameters
    ----------
    fname : str
        Name of file to check.

    Returns
    -------
    bool
        True if it is a geotiff file, False otherwise.
    """
    if splitext(fname)[-1] in [".tif"]:
        return True
    return False


def outputs_match(plugin, output_product, compare_product):
    """Use diff system command to compare currently produced image to correct image.

    Parameters
    ----------
    plugin: OutputCheckerPlugin
        The correspdonding geotiff output_checker - not used but needed in signature
    output_product : str
        Full path to current output product
    compare_product : str
        Full path to comparison product

    Returns
    -------
    bool
        Return True if images match, False if they differ
    """
    # out_diffimg = get_out_diff_fname(compare_product, output_product)

    call_list = ["diff", output_product, compare_product]
    LOG.info("Running %s", " ".join(call_list))
    retval = subprocess.call(call_list)

    # subimg_retval = subprocess.call(call_list)
    if retval != 0:
        LOG.interactive("    *****************************************")
        LOG.interactive("    *** BAD geotiffs do NOT match exactly ***")
        LOG.interactive("    ***   output_product: %s ***", output_product)
        LOG.interactive("    ***   compare_product: %s ***", compare_product)
        LOG.interactive("    *****************************************")
        return False

    LOG.info("    ***************************")
    LOG.info("    *** GOOD geotiffs match ***")
    LOG.info("    ***************************")
    return True


def call(plugin, compare_path, output_products):
    """Compare the "correct" geotiffs found the list of current output_products.

    Compares files produced in the current processing run with the list of
    "correct" files contained in "compare_path".

    Parameters
    ----------
    plugin: OutputCheckerPlugin
        The corresponding geotiff OutputCheckerPlugin that has access to needed methods
    compare_path : str
        Path to directory of "correct" products - filenames must match output_products
    output_products : list of str
        List of strings of current output products,
        to compare with products in compare_path

    Returns
    -------
    int
        Binary code: 0 if all comparisons were completed successfully.
    """
    retval = plugin.compare_outputs(
        compare_path,
        output_products,
    )
    return retval
