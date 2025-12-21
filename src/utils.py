import sys


def local_platform() -> str:
    return {
        "linux": "Linux",
        "linux2": "Linux",
        "win32": "Windows",
        "cygwin": "Windows",
        "msys": "Windows",
        "darwin": "MacOS",
    }.get(sys.platform, sys.platform)
