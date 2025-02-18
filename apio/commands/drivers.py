# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Implementation of 'apio drivers' command"""

from varname import nameof
import click
from click.core import Context
from apio.managers.drivers import Drivers
from apio import cmd_util
from apio.resources import Resources

# ---------------------------
# -- COMMAND SPECIFIC OPTIONS
# ---------------------------
ftdi_install_option = click.option(
    "ftdi_install",  # Var name.
    "--ftdi-install",
    is_flag=True,
    help="Install the FTDI driver.",
    cls=cmd_util.ApioOption,
)

ftdi_uninstall_option = click.option(
    "ftdi_uninstall",  # Var name.
    "--ftdi-uninstall",
    is_flag=True,
    help="Uninstall the FTDI driver.",
    cls=cmd_util.ApioOption,
)

serial_install_option = click.option(
    "serial_install",  # Var name.
    "--serial-install",
    is_flag=True,
    help="Install the Serial driver.",
    cls=cmd_util.ApioOption,
)

serial_uninstall_option = click.option(
    "serial_uninstall",  # Var name.
    "--serial-uninstall",
    is_flag=True,
    help="Uninstall the Serial driver.",
    cls=cmd_util.ApioOption,
)


# ---------------------------
# -- COMMAND
# ---------------------------

HELP = """
The drivers command allows to install or uninstall operating system
drivers that are used to program the FPGA boards. This command is global
and affects all the projects on the local host.

\b
Examples:
  apio drivers --ftdi-install      # Install the FTDI driver.
  apio drivers --ftdi-uninstall    # Uninstall the FTDI driver.
  apio drivers --serial-install    # Install the serial driver.
  apio drivers --serial-uninstall  # Uninstall the serial driver.

  Do not specify more than flag per command invocation.
"""


@click.command(
    "drivers",
    short_help="Manage the operating system drivers.",
    help=HELP,
    cls=cmd_util.ApioCommand,
)
@click.pass_context
@ftdi_install_option
@ftdi_uninstall_option
@serial_install_option
@serial_uninstall_option
def cli(
    ctx: Context,
    # Options:
    ftdi_install: bool,
    ftdi_uninstall: bool,
    serial_install: bool,
    serial_uninstall: bool,
):
    """Implements the drivers command."""

    # Make sure these params are exclusive.
    cmd_util.check_at_most_one_param(
        ctx,
        nameof(ftdi_install, ftdi_uninstall, serial_install, serial_uninstall),
    )

    # -- Access to the Drivers
    resources = Resources(project_scope=False)
    drivers = Drivers(resources)

    # -- FTDI install option
    if ftdi_install:
        exit_code = drivers.ftdi_install()
        ctx.exit(exit_code)

    # -- FTDI uninstall option
    if ftdi_uninstall:
        exit_code = drivers.ftdi_uninstall()
        ctx.exit(exit_code)

    # -- Serial install option
    if serial_install:
        exit_code = drivers.serial_install()
        ctx.exit(exit_code)

    # -- Serial uninstall option
    if serial_uninstall:
        exit_code = drivers.serial_uninstall()
        ctx.exit(exit_code)

    # -- No options. Show the help
    click.secho(ctx.get_help())
