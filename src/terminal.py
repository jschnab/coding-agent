def print_red(txt: str, end="\n") -> None:
    print(f"\033[91m{txt}\033[0m", end=end)


def print_green(txt: str, end="\n") -> None:
    print(f"\033[92m{txt}\033[0m", end=end)


def print_yellow(txt: str, end="\n") -> None:
    print(f"\033[93m{txt}\033[0m", end=end)


def print_blue(txt: str, end="\n") -> None:
    print(f"\033[94m{txt}\033[0m", end=end)


def print_magenta(txt: str, end="\n") -> None:
    print(f"\033[95m{txt}\033[0m", end=end)


def print_cyan(txt: str, end="\n") -> None:
    print(f"\033[96m{txt}\033[0m", end=end)


def reset_terminal_color():
    print("\033[0m", end="")
