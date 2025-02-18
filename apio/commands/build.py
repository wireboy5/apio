# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Implementation of 'apio build' command"""

from pathlib import Path
import click
from click.core import Context
from apio.managers.scons import SCons
from apio import cmd_util
from apio.commands import options
from apio.resources import Resources


# ---------------------------
# -- COMMAND
# ---------------------------

HELP = """
The build command reads the project source files
and generates a bitstream file that you can uploaded to your FPGA.
The commands is typically used in the root directory
of the project that contains the apio.ini file.

\b
Examples:
  apio build       # Build
  apio build -v    # Build with verbose info

The build command builds all the .v files (e.g. my_module.v) in the project
directory except for those whose name ends with _tb (e.g. my_module_tb.v) to
indicate that they are testbenches.
"""


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
@click.command(
    "build",
    short_help="Synthesize the bitstream.",
    help=HELP,
    cls=cmd_util.ApioCommand,
)
@click.pass_context
@options.project_dir_option
@options.verbose_option
@options.verbose_yosys_option
@options.verbose_pnr_option
@options.top_module_option_gen(deprecated=True)
@options.board_option_gen(deprecated=True)
@options.fpga_option_gen(deprecated=True)
@options.size_option_gen(deprecated=True)
@options.type_option_gen(deprecated=True)
@options.pack_option_gen(deprecated=True)
def cli(
    ctx: Context,
    # Options
    project_dir: Path,
    verbose: bool,
    verbose_yosys: bool,
    verbose_pnr: bool,
    # Deprecated options
    top_module: str,
    board: str,
    fpga: str,
    size: str,
    type_: str,
    pack: str,
):
    """Implements the apio build command. It invokes the toolchain
    to syntesize the source files into a bitstream file.
    """

    # The bitstream is generated from the source files (verilog)
    # by means of the scons tool
    # https://www.scons.org/documentation.html

    # -- Create the scons object
    resources = Resources(project_dir=project_dir, project_scope=True)
    scons = SCons(resources)

    # R0801: Similar lines in 2 files
    # pylint: disable=R0801
    # -- Build the project with the given parameters
    exit_code = scons.build(
        {
            "board": board,
            "fpga": fpga,
            "size": size,
            "type": type_,
            "pack": pack,
            "verbose": {
                "all": verbose,
                "yosys": verbose_yosys,
                "pnr": verbose_pnr,
            },
            "top-module": top_module,
        }
    )

    # -- Done!
    ctx.exit(exit_code)


# Advanced notes: https://github.com/FPGAwars/apio/wiki/Commands#apio-build
