import shutil
import subprocess  # noqa: S404
from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class Configuration(object):
    """Configuration object for :class:`~PyHubCtl`."""

    help: bool = field(default=False)
    """Print `uhubctl` help text."""

    action: Union[int, str] = field(default=2)
    """Action to off/on/cycle/toggle (or 0/1/2/3) affected ports."""

    ports: str = field(default="")
    """The ports to operate on (defaults to all ports)."""

    location: str = field(default="")
    """Limit hub by location (defaults to all hubs)."""

    level: str = field(default="")
    """Limit hub by location level (i.e. a-b.c is level 3)."""

    vendor: str = field(default="")
    """Limit hub by vendor id (defaults to all vendors; partial: ok)."""

    search: str = field(default="")
    """Limit hub by attached device description."""

    delay: int = field(default=2)
    """Delay for cycle action (defaults to 2 seconds)."""

    repeat: int = field(default=1)
    """Repeat power off count (defaults to 1).

    Some devices may need this to turn off.
    """

    exact: str = field(default="")
    """Limit hub by exact location (no USB3 duality handling)."""

    force: bool = field(default=False)
    """Force operation even on unsupported hubs."""

    nodesc: bool = field(default=False)
    """Do not query device description (useful for unresponsive devices)."""  # noqa: E501

    reset: bool = field(default=False)
    """Reset hub after each power-on action.

    Causes all devices to re-associate.
    """

    wait: int = field(default=20)  # noqa: WPS432
    """Wait before repeating power off (defaults to 20ms)"""

    version: bool = field(default=False)
    """Print `uhubctl` version."""


class PyHubCtl(object):
    """Interface for controlling `uhubctl` from Python."""

    def run(self, config: Optional[Configuration] = None) -> str:
        """Run `uhubctl` and return its output.

        If `uhubctl` is not installed, a :exc:`~FileNotFoundError` will
        be raised. If `uhubctl` returns an error, a
        :exc:`~subprocess.CalledProcessError` will be raised.

        Args:
            config: The arguments to send to `uhubctl`. If not provided,
                `uhubctl` will be executed without any parameters. The
                result will be what USB hubs the program could locate.

        Returns:
            The output from `uhubctl`.
        """
        # Verify the utility is installed
        self._check_installed()

        # If no config was provided, just run the utility
        if not config:
            return self._run("")

        # A config was provided, so build arguments from this
        args = self._build_args_from_config(config)

        # Run the program and return its output
        return self._run(args)

    def _build_args_from_config(  # noqa: C901, WPS231
        self,
        config: Configuration,
    ) -> str:
        prog_args = ""

        # Only print the help text
        if config.help:
            return "-h"

        # Only print the version
        if config.version:
            return "-v"

        if config.action:
            prog_args += "-a {action}".format(action=config.action)
        else:
            raise ValueError("arg 'action' must be set")

        if config.ports:
            prog_args += " -p {ports}".format(ports=config.ports)

        if config.location:
            prog_args += " -l {location}".format(location=config.location)

        if config.level:
            prog_args += " -L {level}".format(level=config.level)

        if config.vendor:
            prog_args += " -n {vendor}".format(vendor=config.vendor)

        if config.search:
            prog_args += " -s {search}".format(search=config.search)

        if config.delay:
            prog_args += " -d {delay}".format(delay=config.delay)

        if config.repeat:
            prog_args += " -r {repeat}".format(repeat=config.repeat)

        if config.exact:
            prog_args += " -e {exact}".format(exact=config.exact)

        if config.force:
            prog_args += " -f {force}".format(force=config.force)

        if config.nodesc:
            prog_args += " -N {nodesc}".format(nodesc=config.nodesc)

        if config.reset:
            prog_args += " -R {reset}".format(reset=config.reset)

        if config.wait:
            prog_args += " -w {wait}".format(wait=config.wait)

        return prog_args

    def _check_installed(self) -> None:
        if not shutil.which("uhubctl"):
            raise FileNotFoundError(
                "uhubctl is not installed (or on PATH). Install it by "
                + "following these directions: https://github.com/mvp/uhubctl#compiling",
            )

    def _run(self, args: str) -> str:
        # Convert the string of args to a list
        cmd = ["uhubctl", *args.split(" ")] if args else ["uhubctl"]

        # Run the program
        # Apparently -h returns a 1 for an exit code, so add
        # compatibility for it; otherwise, raise an error when other
        # actions are executed and they return a non-zero code
        proc = subprocess.run(  # noqa: S603
            cmd,
            check="-h" not in cmd,
            capture_output=True,
        )
        return proc.stdout.decode()
