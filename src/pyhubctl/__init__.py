import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

dist_name = __name__
try:
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


from pyhubctl.pyhubctl import Configuration, PyHubCtl  # noqa: E402

__all__ = (  # noqa: WPS410
    "Configuration",
    "PyHubCtl",
)
