# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Implementation of 'apio graph' command"""

from pathlib import Path
import click
from click.core import Context
from varname import nameof
from apio.managers.scons import SCons
from apio import cmd_util
from apio.commands import options
from apio.resources import Resources

# ---------------------------
# -- COMMAND SPECIFIC OPTIONS
# ---------------------------


pdf_option = click.option(
    "pdf",  # Var name.
    "--pdf",
    is_flag=True,
    help="Generate a pdf file.",
    cls=cmd_util.ApioOption,
)

png_option = click.option(
    "png",  # Var name.
    "--png",
    is_flag=True,
    help="Generate a png file.",
    cls=cmd_util.ApioOption,
)


# ---------------------------
# -- COMMAND
# ---------------------------
HELP = """
The graph command generates a graphical representation of
the verilog code of the project. The commands is typically
used in the root directory of the project that contains
the apio.ini file.

\b
Examples:
  apio graph               # Generate a svg file.
  apio graph --pdf         # Generate a pdf file.
  apio graph --png         # Generate a png file.
  apio graph -t my_module  # Graph my_module module.

"""

EPILOG = """
[Hint] On windows, type 'explorer hardware.svg' to
view the graph, and on Mac OS type 'open hardware.svg'.
"""


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
@click.command(
    "graph",
    short_help="Generate a visual graph of the code.",
    help=HELP,
    epilog=EPILOG,
    cls=cmd_util.ApioCommand,
)
@click.pass_context
@pdf_option
@png_option
@options.project_dir_option
@options.top_module_option_gen(help="Set the name of the top module to graph.")
@options.verbose_option
def cli(
    ctx: Context,
    # Options
    pdf: bool,
    png: bool,
    project_dir: Path,
    verbose: bool,
    top_module: str,
):
    """Implements the apio graph command."""
    # -- Sanity check the options.
    cmd_util.check_at_most_one_param(ctx, nameof(pdf, png))

    # -- Construct the graph spec to pass to scons.
    # -- For now it's trivial.
    if pdf:
        graph_spec = "pdf"
    elif png:
        graph_spec = "png"
    else:
        graph_spec = "svg"

    # -- Load apio resources.
    resources = Resources(project_dir=project_dir, project_scope=True)

    # -- Create the scons object.
    scons = SCons(resources)

    # -- Graph the project with the given parameters
    exit_code = scons.graph(
        {
            "verbose": {"all": verbose, "yosys": False, "pnr": False},
            "top-module": top_module,
            "graph_spec": graph_spec,
        }
    )

    # -- Done!
    ctx.exit(exit_code)
