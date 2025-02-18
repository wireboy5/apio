# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Implementation of 'apio create' command"""

from pathlib import Path
import click
from click.core import Context
from apio.managers.project import Project, DEFAULT_TOP_MODULE, PROJECT_FILENAME
from apio import util
from apio import cmd_util
from apio.commands import options
from apio.resources import Resources


# ---------------------------
# -- COMMAND
# ---------------------------
HELP = f"""
The create command creates the project file apio.ini from scratch.
The commands is typically used in the root directory
of the project where the apio.ini file is created.

\b
Examples:
  apio create --board icezum
  apio create --board icezum --top-module MyModule
  apio create --board icezum --sayyes

The flag --board is required. The flag --top-module is optional and has
the default '{DEFAULT_TOP_MODULE}'. If the file apio.ini already exists
the command asks for permision to delete it. If --sayyes is specified,
the file is deleted automatically.

[Note] this command creates just the '{PROJECT_FILENAME}' file
rather than a full buildable project.
Some users use instead the examples command to copy a working
project for their board, and then modify it with with their design.

[Hint] Use the command 'apio examples -l' to see a list of
the supported boards.
"""


# R0913: Too many arguments (6/5)
# pylint: disable=R0913
@click.command(
    "create",
    short_help="Create an apio.ini project file.",
    help=HELP,
    cls=cmd_util.ApioCommand,
)
@click.pass_context
@options.board_option_gen(help="Set the board.", required=True)
@options.top_module_option_gen(help="Set the top level module name.")
@options.project_dir_option
@options.sayyes
def cli(
    ctx: Context,
    # Options
    board: str,
    top_module: str,
    project_dir: Path,
    sayyes: bool,
):
    """Create a project file."""

    # Board is annotated above as required so must exist.
    assert board is not None

    if not top_module:
        top_module = DEFAULT_TOP_MODULE

    # -- Load resources. We use project scope in case the project dir
    # -- already has a custom boards.json file so we validate 'board'
    # -- against that board list.
    resources = Resources(project_dir=project_dir, project_scope=True)

    project_dir = util.get_project_dir(project_dir)

    # Create the apio.ini file
    ok = Project.create_ini(resources, board, top_module, sayyes)

    exit_code = 0 if ok else 1
    ctx.exit(exit_code)
