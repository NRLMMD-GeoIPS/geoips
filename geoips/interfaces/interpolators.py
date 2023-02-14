from geoips.interfaces.base import BaseInterface, BasePlugin


class InterpolatorsInterface(BaseInterface):
    name = "interpolators"
    entry_point_group = "interpolation"
    deprecated_family_attr = "interp_type"
    required_args = {'2d': ['area_def', 'input_xarray', 'output_xarray', 'varlist'],
                     'grid': ['area_def', 'input_xarray', 'output_xarray', 'varlist']}


interpolators = InterpolatorsInterface()

