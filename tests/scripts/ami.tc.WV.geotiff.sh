#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

# Default values - if you do not have this exact test case available, call with available data files / sectors.

# This exact test case required for valid comparisons - remove "compare_path" argument if running a different
# set of arguments.
run_procflow $GEOIPS_TESTDATA_DIR/test_data_noaa_aws/data/geokompsat/20231208/0300/*.nc \
          --procflow single_source \
          --reader_name ami_netcdf \
          --product_name WV \
          --filename_formatter geotiff_fname \
          --output_formatter geotiff_standard \
          --trackfile_parser bdeck_parser \
          --trackfiles $GEOIPS_PACKAGES_DIR/geoips/tests/sectors/tc_bdecks/bsh032024.dat \
          --compare_path "$GEOIPS_PACKAGES_DIR/geoips/tests/outputs/ami.tc.<product>.geotiff" \
          --resampled_read
retval=$?

exit $retval
