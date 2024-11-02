"""Processing workflow for order based data source processing."""

from argparse import ArgumentParser
import yaml

from geoips import interfaces
from geoips.pydantic.products import ProductPlugin


interface = "procflows"
family = "standard"
name = "order_based"


def call(
    fnames: list[str], product_path: str, command_line_args: list[str] | None = None
) -> None:
    """Run the order based procflow.

    Runs an OBP processing with the specified input data files &
    steps listed in product definition file (PDF).

    Parameters
    ----------
    fnames : (list[str])
        list of filenames to process
    product-path : (str)
        path to the product definition file
    command_line_args : (list[str] | None, optional)
        fnames & product-path

    Returns
    -------
        * None
    """
    with open(product_path) as product_definition_file:
        prod_dict = yaml.safe_load(product_definition_file)
        prod = ProductPlugin(**prod_dict)

    for step in prod.spec.steps:
        step_def = step.definition
        print(
            # f"\n\nstep\t {step} \n\nplugin \n\t"
            f"\n\t type : {step_def.type}"
            f"\n\t name : {step_def.name} \n\t arguments : {step_def.arguments}"
        )

        interface = step_def.type + "s"
        plugin_instance = getattr(interfaces, interface, None).get_plugin(step_def.name)

        print(
            f"\n\n{step_def.type} processing details:\n\n\t"
            f"{plugin_instance(fnames, step_def.arguments)}\n\n"
        )


if __name__ == "__main__":

    parser = ArgumentParser(description="order-based procflow processing")
    parser.add_argument("fnames", nargs="+", help="The filenames to process.")
    parser.add_argument("-p", "--product_path", help="The path to the PDF.")

    args = parser.parse_args()
    call(args.fnames, args.product_path)
