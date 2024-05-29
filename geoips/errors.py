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

"""GeoIPS error module."""


class AsciiPaletteError(Exception):
    """Exception to be raised when encountering an invalid ascii palette text file."""

    pass


class EntryPointError(Exception):
    """Exception to be raised when an entry-point cannot be found."""

    pass

  
class PluginError(Exception):
    """Exception to be raised when there is an error in a GeoIPS plugin."""

    pass


class PluginRegistryError(Exception):
    """Exception to be raised when there is an error in a plugin registry."""

    pass


class PluginValidationError(Exception):
    """Exception to be raised when a plugin found in the registry is not valid."""

    pass


class CoverageError(Exception):
    """Raise exception on data coverage error."""

    pass


class CliError(Exception):
    """Raise exception on command line interface error."""

    pass
