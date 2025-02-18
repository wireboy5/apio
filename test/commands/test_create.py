"""
  Test for the "apio create" command
"""

from pathlib import Path
from os.path import isfile, exists
from typing import Dict
from configobj import ConfigObj

# -- apio create entry point
from apio.commands.create import cli as cmd_create


# R0801: Similar lines in 2 files
# pylint: disable=R0801
def check_ini_file(apio_ini: Path, expected_vars: Dict[str, str]) -> None:
    """Assert that apio.ini contains exactly the given vars."""
    # Read the ini file.
    assert isfile(apio_ini)
    conf = ConfigObj(str(apio_ini))
    # Check the expected comment at the top.
    assert "# APIO project configuration file" in conf.initial_comment[0]
    # Check the expected vars.
    assert conf.dict() == {"env": expected_vars}


def test_create(clirunner, configenv, validate_cliresult):
    """Test "apio create" with different parameters"""

    with clirunner.isolated_filesystem():

        # -- Config the environment (conftest.configenv())
        configenv()

        apio_ini = Path("apio.ini")
        assert not exists(apio_ini)

        # -- Execute "apio create"
        result = clirunner.invoke(cmd_create)
        assert result.exit_code != 0, result.output
        assert "Error: Missing option" in result.output
        assert not exists(apio_ini)

        # -- Execute "apio create --board missed_board"
        result = clirunner.invoke(cmd_create, ["--board", "missed_board"])
        assert result.exit_code == 1, result.output
        assert "Error: no such board" in result.output
        assert not exists(apio_ini)

        # -- Execute "apio create --board icezum"
        result = clirunner.invoke(cmd_create, ["--board", "icezum"])
        validate_cliresult(result)
        assert "Creating apio.ini file ..." in result.output
        assert "was created successfully." in result.output
        check_ini_file(apio_ini, {"board": "icezum", "top-module": "main"})

        # -- Execute "apio create --board alhambra-ii
        # --                      --top-module my_module" with 'y' input"
        result = clirunner.invoke(
            cmd_create,
            ["--board", "alhambra-ii", "--top-module", "my_module"],
            input="y",
        )
        validate_cliresult(result)
        assert "Warning" in result.output
        assert "file already exists" in result.output
        assert "Do you want to replace it?" in result.output
        assert "was created successfully." in result.output
        check_ini_file(
            apio_ini, {"board": "alhambra-ii", "top-module": "my_module"}
        )

        # -- Execute "apio create --board icezum
        # --                      --top-module my_module
        # --                      --sayyse" with 'y' input
        result = clirunner.invoke(
            cmd_create,
            ["--board", "icezum", "--top-module", "my_module", "--sayyes"],
        )
        validate_cliresult(result)
        assert "was created successfully." in result.output
        check_ini_file(
            apio_ini, {"board": "icezum", "top-module": "my_module"}
        )

        # -- Execute "apio create --board alhambra-ii
        # --                      --top-module my_module" with 'n' input
        result = clirunner.invoke(
            cmd_create,
            ["--board", "alhambra-ii", "--top-module", "my_module"],
            input="n",
        )
        assert result.exit_code != 0, result.output
        assert "Warning" in result.output
        assert "file already exists" in result.output
        assert "Do you want to replace it?" in result.output
        assert "Abort!" in result.output
        check_ini_file(
            apio_ini, {"board": "icezum", "top-module": "my_module"}
        )
