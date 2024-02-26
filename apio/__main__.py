"""APIO ENTRY POINT"""

# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

# --------------------------------------------
# -- Apio ENTRY POINT!!!
# --------------------------------------------

import string
import click

from apio import util


# -- Get the commands folder
commands_folder = util.get_full_path("commands")


def find_commands_help(help_list, commands):
    """
    Return a list with the given commands and their descriptions.
    This information is read from the given help list of string
    - INPUTS:
      * help_list: A list of help lines (strings)
      * commands: A list of commands (strings) to obtain their descriptions
    """

    # -- List to return
    commands_help = []

    # -- Analyze all the lines in the help string
    for line in help_list:
        # -- Check all the commands passed
        for command in commands:
            # -- If the command is in the current line of the help string
            if f" {command}" in line:
                # -- Add the  and its description to the list of commands
                commands_help.append(line)

    # -- Return the list of comands with their descriptions
    return commands_help


# -----------------------------------------------------------------------------
# -- Main Click Class
# -- It is extended for including methods for getting and listing the commands
# -----------------------------------------------------------------------------
class ApioCLI(click.MultiCommand):
    """DOC:TODO"""

    # -- Return  a list of all the available commands
    def list_commands(self, ctx):
        # -- All the python files inside the apio/commands folder are commands,
        # -- except __init__.py
        # -- Create the list
        cmd_list = [
            element.stem  # -- Name without path and extension
            for element in commands_folder.iterdir()
            if element.is_file()
            and element.suffix == ".py"
            and element.stem != "__init__"
        ]

        cmd_list.sort()
        return cmd_list

    # -- Return the code function (cli) of the command name
    # -- This cli function is called whenever the name command
    # -- is issued
    # -- INPUT:
    # --   * cmd_name: Apio command name
    def get_command(self, ctx, cmd_name: string):
        nnss = {}

        # -- Get the python filename asociated with the give command
        # -- Ex. "system" --> "/home/obijuan/.../apio/commands/system.py"
        filename = commands_folder / f"{cmd_name}.py"

        # -- Check if the file exists
        if filename.exists():
            # -- Open the python file
            with filename.open(encoding="utf8") as file:
                # -- Compile it!
                code = compile(file.read(), filename, "exec")

                # -- Get the function!
                # pylint: disable=W0123
                eval(code, nnss, nnss)

        # -- Return the function needed for executing the command
        return nnss.get("cli")


# ------------------------------------------------------------------
# -- This function is executed when apio is executed without
# -- any parameter. The help is shown
# ------------------------------------------------------------------
@click.command(cls=ApioCLI, invoke_without_command=True, context_settings=util.context_settings())
@click.pass_context
@click.version_option()
def cli(ctx):
    """Work with FPGAs with ease"""

    # -- No command typed: show help
    if ctx.invoked_subcommand is None:
        # -- The help string is automatically generated by Click
        # -- It could be directly printed on the console but...
        _help = ctx.get_help()

        # -- Let's change the format so that the commands are divided
        # -- into three categories: Project, Setup and Utilities
        # -- Convert the help string into a list of lines
        _help = _help.split("\n")

        # -- Setup commands
        setup_help = find_commands_help(
            _help, ["drivers", "init", "install", "uninstall"]
        )

        # -- Utility commands
        util_help = find_commands_help(
            _help, ["boards", "config", "examples", "raw", "system", "upgrade"]
        )

        # -- Reformat the Help string
        _help = "\n".join(_help)
        _help = _help.replace("Commands:\n", "Project commands:\n")
        _help += "\n\nSetup commands:\n"
        _help += "\n".join(setup_help)
        _help += "\n\nUtility commands:\n"
        _help += "\n".join(util_help)
        _help += "\n"

        click.secho(_help)

    # -- If there is a command, it is executed when this function is finished
    # -- Debug: print the command invoked
    # print(f"{ctx.invoked_subcommand}")
