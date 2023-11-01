"""Generates all available plugins from all installed GeoIPS packages.

After all plugins have been generated, they are written to a registered_plugins.yaml
file which contains a dictionary of all the registered GeoIPS plugins.

To use this module, simply call 'python create_plugin_registry.py'.
The main function will do the rest!
"""

from importlib import resources
import os
import logging
from geoips.errors import PluginRegistryError

LOG = logging.getLogger(__name__)


class PluginRegistry:
    """Plugin Registry class definition.

    Represents all of the plugins found in all of the available GeoIPS packages.
    This class will load a plugin when requested, rather than loading all plugins when
    GeoIPS is instantiated.
    """

    def __init__(self, _test_registry_files=[]):
        # Use this for unit testing
        if _test_registry_files:
            self.registry_files = _test_registry_files
            self._is_test = True
        # Use this for normal operation and collect the registry files
        else:
            from geoips.geoips_utils import get_entry_point_group

            self._is_test = False
            self.registry_files = []  # Collect the paths to the registry files here
            for pkg in get_entry_point_group("geoips.plugin_packages"):
                self.registry_files.append(
                    str(resources.files(pkg.value) / "registered_plugins")
                )

    @property
    def registered_plugins(self):
        """Plugin Registry registered_plugins attribute."""
        if not hasattr(self, "_registered_plugins"):
            self._set_class_properties()
        return self._registered_plugins

    @property
    def interface_mapping(self):
        """Plugin Registry interface_mapping attribute."""
        if not hasattr(self, "_interface_mapping"):
            self._set_class_properties()
        return self._interface_mapping

    def _set_class_properties(self):
        """Find all plugins in registered plugin packages.

        Search the ``registered_plugins.yaml`` of each registered plugin package and add
        them to the _registered_plugins dictionary
        """
        # Load the registries here and return them as a dictionary
        if not hasattr(self, "_registered_plugins"):
            from geoips.geoips_utils import merge_nested_dicts
            import pickle  # nosec
            import yaml

            # Complete dictionary of all available plugins found in every geoips package
            self._registered_plugins = {}
            # A mapping of interfaces to plugin_types. Ie:
            # {
            # "yaml_based": [products, sectors, ...],
            # "module_based": [algorithms, readers, ...],
            # "text_based": [tpw_cimss, ...]
            # }
            self._interface_mapping = {}
            for reg_path in self.registry_files:
                if not os.path.exists(reg_path):
                    raise PluginRegistryError(
                        f"Plugin registry {reg_path} did not exist, "
                        "please run 'create_plugin_registries'"
                    )
                # This will include all plugins, including schemas, yaml_based,
                # and module_based plugins.
                if self._is_test:
                    pkg_plugins = yaml.safe_load(open(reg_path, "r"))
                else:
                    pkg_plugins = pickle.load(open(reg_path, "rb"))  # nosec
                try:
                    self.ensure_plugin_types_exist(pkg_plugins, reg_path)
                except PluginRegistryError as e:
                    print(e)
                try:
                    for plugin_type in pkg_plugins:
                        if plugin_type not in self._registered_plugins:
                            self._registered_plugins[plugin_type] = {}
                            self._interface_mapping[plugin_type] = []
                        for interface in pkg_plugins[plugin_type]:
                            interface_dict = pkg_plugins[plugin_type][interface]
                            if interface not in self._registered_plugins[plugin_type]:
                                self._registered_plugins[plugin_type][
                                    interface
                                ] = interface_dict  # NOQA
                                self._interface_mapping[plugin_type].append(interface)
                            else:
                                merge_nested_dicts(
                                    self._registered_plugins[plugin_type][interface],
                                    interface_dict,
                                )
                except TypeError:
                    raise PluginRegistryError(f"Failed reading {reg_path}.")
        return self._registered_plugins

    def get_plugin_info(self, interface, plugin_name):
        """Find a plugin in the registry and return its info.

        This should remove all plugin loading from the base interfaces and allow us
        to only load one plugin at a time
        """
        plugin_type = self.identify_plugin_type(interface)
        if isinstance(plugin_name, tuple):
            return self.registered_plugins[plugin_type][interface][plugin_name[0]][
                plugin_name[1]
            ]
        return self.registered_plugins[plugin_type][interface][plugin_name]

    def get_interface_plugin_info(self, interface):
        """Find an interface in the registry and return its corresponding info.

        This should remove all plugin loading from the base interfaces and allow us
        to only load one plugin at a time
        """
        plugin_type = self.identify_plugin_type(interface)
        return self.registered_plugins[plugin_type][interface]

    def get_interface_plugin_names(self, interface):
        """List all available plugins in the an interface of the registry.

        This should remove all plugin loading from the base interfaces and allow us
        to only load one plugin at a time
        """
        plugin_type = self.identify_plugin_type(interface)
        return list(self.registered_plugins[plugin_type][interface].keys())

    def list_plugins(self, interface):
        """List the plugins available for an interface ONLY based on the registries.

        This should not load any plugins, just return info from the registries.
        """
        plugin_type = self.identify_plugin_type(interface)
        return self.registered_plugins[plugin_type][interface]

    def identify_plugin_type(self, interface):
        """Identify the Plugin Type based on the provided interface."""
        plugin_type = None
        for p_type in self.interface_mapping:
            if interface in self.interface_mapping[p_type]:
                plugin_type = p_type
                break
        if plugin_type is None:
            raise PluginRegistryError(
                f"{interface} does not exist within any package registry."
            )
        return plugin_type

    def ensure_plugin_types_exist(self, reg_dict, reg_path):
        """Test that all top level plugin types exist in each registry file."""
        expected_plugin_types = ["yaml_based", "module_based", "text_based"]
        for p_type in expected_plugin_types:
            if p_type not in reg_dict:
                error_str = f"Expected plugin type '{p_type}' to be in the registry but"
                error_str += f" wasn't. This was in file '{reg_path}'."
                raise PluginRegistryError(error_str)


plugin_registry = PluginRegistry()
