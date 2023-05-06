"""Products interface module."""

import logging
from geoips.geoips_utils import merge_nested_dicts
from geoips.interfaces.base import YamlPluginValidator, BaseYamlInterface
from geoips.interfaces.yaml_based.product_defaults import product_defaults
from jsonschema.exceptions import ValidationError

LOG = logging.getLogger(__name__)


class ProductsPluginValidator(YamlPluginValidator):
    """Validator for Products plugins.

    This differs from other validators for two reasons:

    1. Most plugins are identified solely by 'name'. Products are identified by
       'source_name' and 'name.
    2. Most plugins supply their 'family' directly. Products can supply it directly, but
       can, alternatively, specify a 'product_defaults' plugin from which to pull
       'family' and most other properties. This validator handles filling in a product
       plugin based on its specified product defaults plugin.
    """

    def validate(self, plugin, validator_id=None):
        """Validate a Products plugin against the relevant schema.

        The relevant schema is determined based on the interface and family of the
        plugin.
        """
        if "product_defaults" in plugin:
            if "family" in plugin:
                raise ValidationError(
                    "Properties 'family' and 'product_defaults' are mutually exclusive."
                )
            self.validate_product(plugin)
        else:
            plugin = super().validate(plugin, validator_id=validator_id)

        return plugin

    def validate_product(self, product):
        """Validate single product."""
        LOG.debug("In validate product")
        if "family" in product:
            LOG.debug("Validating family-based product")
            family = product["family"]
            try:
                spec_validator = self.validators[f"product_defaults.specs.{family}"]
            except KeyError:
                raise ValidationError(
                    f"No product_defaults spec for family {family}", instance=product
                )
            spec_validator.validate(product["spec"])
        elif "product_defaults" in product:
            defaults = product_defaults.get_plugin(product.pop("product_defaults"))
            product["family"] = defaults["family"]

            LOG.debug("Validating product_defaults-based product")
            # This updates missing values in spec from defaults but leaves existing
            # values alone. Using update here ensures that we're updating in-place
            # rather than creating a new dictionary.
            merge_nested_dicts(product, defaults)
        else:
            raise ValidationError(
                f"Product {product['name']} did not specify either "
                f"'family' or 'product_defaults'."
            )
        return product


class ProductsInterface(BaseYamlInterface):
    """GeoIPS interface for Products plugins."""

    name = "products"
    validator = ProductsPluginValidator()

    @staticmethod
    def _create_plugin_cache_name(yaml_plugin):
        """Create a plugin name for cache storage.

        This name is a tuple containing source_name and name.

        Overrides the same method from YamlPluginValidator.
        """
        return (yaml_plugin["source_name"], yaml_plugin["name"])

    def get_plugin(self, source_name, name, product_spec_override=None):
        """Retrieve a Product plugin by source_name, name, and product_spec_override.

        If product_spec_override dict is passed, values contained within
        product_spec_override will be used in place of those found in products
        list and product_defaults.

        product_spec_override[product_name] matches the format of the product
        "spec" field.

        Additionall, if the special key product_spec_override["all"] is included,
        it will apply to all products not specified by name within the dictionary.
        """
        prod_plugin = super().get_plugin((source_name, name))
        if product_spec_override is not None:
            # Default to no override arguments
            override_args = {}
            # If available, use the current product's override values
            if name in product_spec_override:
                override_args = product_spec_override[name]
            # Otherwise, if "all" specified, use those override values
            elif "all" in product_spec_override:
                override_args = product_spec_override["all"]
            prod_plugin["spec"] = merge_nested_dicts(
                prod_plugin["spec"], override_args, in_place=False
            )

        return prod_plugin

    def get_plugins(self):
        """Retrieve a plugin by name."""
        plugins = []
        for source_name, name in self._unvalidated_plugins.keys():
            plugins.append(self.get_plugin(source_name, name))
        return plugins


products = ProductsInterface()
