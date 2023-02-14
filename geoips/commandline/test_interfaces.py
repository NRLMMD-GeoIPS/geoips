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
"""Simple test script to run "test_<interface>_interface" for each interface.

This includes both dev and stable interfaces.
Note this will be deprecated with v2.0 - replaced with a new class-based
interface implementation.
"""
import pprint
from importlib import import_module
import traceback


def main():
    """Script to test all dev and stable interfaces."""
    # Removed all interfaces that have been moved to new setup.
    # This entire testing construct will be updated in the future to more fully
    # test/validate the plugins.
    interfaces = [
        "interfaces.algorithms",
        "dev.boundaries",
        "interfaces.colormaps",
        "interfaces.filename_formats",
        "dev.gridlines",
        "interfaces.interpolators",
        "interfaces.output_formats",
        "interfaces.procflows",
        #"dev.product",
        "interfaces.readers",
        "interfaces.title_formats",
    ]

    interface_name_outliers = {'Boundaries': 'Map',
                               'Colormaps': 'ColorMaps',
                               'TitleFormats': 'TitleFormatters',
                               }

    for curr_interface in interfaces:
        #interface_name = curr_interface.split(".")[1]
        raw_interface_name = curr_interface.split(".")[1]

        interface_name = "".join([name.capitalize() for name in raw_interface_name.split('_')])

        if interface_name in interface_name_outliers:
            interface_name = interface_name_outliers[interface_name]

        print("")
        print(f"Testing {curr_interface}...")
        print("ipython")

        try:
            test_curr_interface = getattr(
                import_module(f"geoips.{curr_interface}"),
                f"{interface_name}Interface",
            )
            print(
                f"    from geoips.{curr_interface} import {interface_name}Interface"
            )
            print(f"    {interface_name}Interface()")

            curr_class = test_curr_interface()
            
            try:
                out_dict = curr_class.test_interface_plugins()
            except Exception:
                print(traceback.format_exc())
                raise
        except AttributeError:
            interface_name = raw_interface_name

            test_curr_interface = getattr(
                import_module(f"geoips.{curr_interface}"),
                f"test_{interface_name}_interface",
            )
            print(
                f"    from geoips.{curr_interface} import test_{interface_name}_interface"
            )
            print(f"    test_{interface_name}_interface()")

            try:
                out_dict = test_curr_interface()
            except Exception:
                print(traceback.format_exc())
                raise




        #from geoips.interfaces.algorithms import AlgorithmsInterface
        #alg = AlgorithmsInterface()
        #out_dict = alg.test_interface_plugins()



        print(f"SUCCESSFUL INTERFACE {curr_interface}")

        ppprinter = pprint.PrettyPrinter(indent=2)
        ppprinter.pprint(out_dict)

        for modname in out_dict["validity_check"]:
            if not out_dict["validity_check"][modname]:
                print(f"FAILED INTERFACE {curr_interface} on {modname}")
                raise TypeError(
                    f"Failed validity check on {modname} in interface {curr_interface}"
                )


if __name__ == "__main__":
    main()
