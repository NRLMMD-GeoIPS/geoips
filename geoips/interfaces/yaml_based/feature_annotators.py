# # # Distribution Statement A. Approved for public release. Distribution is unlimited.
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

"""Feature Annotator interface module."""

from geoips.interfaces.base import BaseYamlInterface


class FeatureAnnotatorsInterface(BaseYamlInterface):
    """Interface for feature annotator plugins."""

    name = "feature_annotators"


feature_annotators = FeatureAnnotatorsInterface()
