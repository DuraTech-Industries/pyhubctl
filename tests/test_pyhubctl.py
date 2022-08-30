from contextlib import suppress
import subprocess
import pytest
from pyhubctl import Configuration, PyHubCtl

def test_program_not_installed() -> None:
    """Verify an error is raised when `uhubctl` cannot be found."""
    import os
    import pathlib
    import shutil

    # Deliberately remove every occurrence where uhubctl exists on path
    current_path = os.environ["PATH"]
    while True:
        which = shutil.which("uhubctl")
        if not which:
            break

        parent = pathlib.Path(which).parent
        os.environ["PATH"] = os.environ["PATH"].replace(str(parent), "")

    phc = PyHubCtl()
    try:
        with pytest.raises(FileNotFoundError):
            phc.run()
    finally:
        os.environ["PATH"] = current_path


def test_normal_exec() -> None:
    """Verify `uhubctl` runs normally."""
    # Note: These configurations are specific to one environment. You
    # may need to change these values if you are getting errors while
    # running tests.
    config = Configuration(location="1-4")
    phc = PyHubCtl()

    phc.run()
    phc.run(config)

    # Configure everything, its okay if this raises an error
    with suppress(subprocess.CalledProcessError):
        config2 = Configuration(
            ports="3,4",
            location="1-4",
            level="1-4.4",
            vendor="abcd:1234",
            search="highspeed enable connect",
            exact="0bda:5411",
            force=True,
            nodesc=True,
            reset=True,
        )
        phc.run(config2)

    phc.run(Configuration(help=True))
    phc.run(Configuration(version=True))
    with pytest.raises(ValueError):
        phc.run(Configuration(action=None))

    with pytest.raises(subprocess.CalledProcessError):
        phc.run(Configuration(location=""))

    with pytest.raises(subprocess.CalledProcessError):
        phc.run(Configuration(delay=0))

    with pytest.raises(subprocess.CalledProcessError):
        phc.run(Configuration(repeat=0))

    with pytest.raises(subprocess.CalledProcessError):
        phc.run(Configuration(wait=0))
