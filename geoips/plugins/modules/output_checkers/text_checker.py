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
from geoips.plugins.modules.output_checkers.utils import compare_outputs as co

LOG = logging.getLogger(__name__)

interface = "output_checkers"
family = "standard"
name = "text_checker"


def correct_type(fname):
    """Check if fname is a text file.

    Parameters
    ----------
    fname : str
        Name of file to check.

    Returns
    -------
    bool
        True if it is a text file, False otherwise.
    """
    if splitext(fname)[-1] in ["", ".txt", ".text", ".yaml"]:
        with open(fname) as f:
            line = f.readline()
        if isinstance(line, str):
            return True
    return False


def text_match(output_product, compare_product):
    """Check if two text files match.

    Parameters
    ----------
    output_product : str
        Full path to current output product
    compare_product : str
        Full path to "good" comparison product

    Returns
    -------
    bool
        Return True if products match, False if they differ
    """
    ret = subprocess.run(
        ["diff", output_product, compare_product],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    LOG.debug(ret.stdout)
    if ret.returncode == 0:
        LOG.info("    *****************************")
        LOG.info("    *** GOOD Text files match ***")
        LOG.info("    *****************************")
        return True

    out_difftxt = co.get_out_diff_fname(compare_product, output_product)
    with open(out_difftxt, "w") as fobj:
        subprocess.call(["diff", output_product, compare_product], stdout=fobj)
    LOG.interactive("    *******************************************")
    LOG.interactive("    *** BAD Text files do NOT match exactly ***")
    LOG.interactive("    ***   output_product: %s ***", output_product)
    LOG.interactive("    ***   compare_product: %s ***", compare_product)
    LOG.interactive("    ***   out_difftxt: %s ***", out_difftxt)
    LOG.interactive("    *******************************************")
    return False


def call(compare_path, output_products, test_product_func=None):
    """Compare the "correct" imagery found the list of current output_products.

    Compares files produced in the current processing run with the list of
    "correct" files contained in "compare_path".

    Parameters
    ----------
    compare_path : str
        Path to directory of "correct" products - filenames must match output_products
    output_products : list of str
        List of strings of current output products,
        to compare with products in compare_path
    test_product_func : function, default=None
        Alternative function to be used for testing output product

          * Call signature must be:

              * output_product, compare_product, goodcomps, badcomps, compare_strings

          * Return must be:

              * goodcomps, badcomps, compare_strings

        * If None, use geoips.compare_outputs.test_product)

    Returns
    -------
    int
        Binary code: 0 if all comparisons were completed successfully.
    """
    retval = co.compare_outputs(compare_path, output_products, test_product_func)
    return retval
