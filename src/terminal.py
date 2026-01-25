from functools import partial

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET_COLOR = "\033[0m"


def reset_terminal_color():
    print(RESET_COLOR, end="")


def maybe_reset_color(reset: bool) -> str:
    if reset:
        return RESET_COLOR
    return ""


def print_with_color(
    txt: str,
    color: str,
    end: str ="\n",
    reset_color: bool = True,
) -> None:
    print(f"{color}{txt}{maybe_reset_color(reset_color)}", end=end)


print_red = partial(print_with_color, color=RED)
print_green = partial(print_with_color, color=GREEN)
print_yellow = partial(print_with_color, color=YELLOW)
print_blue = partial(print_with_color, color=BLUE)
print_magenta = partial(print_with_color, color=MAGENTA)
print_cyan = partial(print_with_color, color=CYAN)
