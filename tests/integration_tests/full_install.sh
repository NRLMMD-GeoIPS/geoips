# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

test_exit=""
install_script=""
if [[ "$1" == "exit_on_missing" ]]; then
    test_exit="exit_on_missing"
    install_script="$0"
fi

. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh geoips_full
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh ancillary_data cartopy_shapefiles $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh source_repo geoips $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh source_repo data_fusion $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh source_repo recenter_tc $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh source_repo geoips_clavrx $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh source_repo geoips_plugin_example $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh source_repo template_basic_plugin $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh settings_repo .vscode $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_noaa_aws $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_amsr2 $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_clavrx $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_gpm $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_sar $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_scat $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_smap $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_viirs $test_exit $install_script
. $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh test_data test_data_fusion $test_exit $install_script
create_plugin_registries
