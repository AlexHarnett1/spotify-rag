verbose_logging = True

def vprint(*args, **kwargs):
    if verbose_logging:
        YELLOW = "\033[33m"
        RESET = "\033[0m"
        print(f"{YELLOW}", end="")
        print(*args, **kwargs)
        print(f"{RESET}", end="")

def bot_print(*args, **kwargs):
    if verbose_logging:
        BLUE = "\033[34m"
        RESET = "\033[0m"
        print(f"{BLUE}", end="")
        print(*args, **kwargs)
        print(f"{RESET}", end="")

def human_print(*args, **kwargs):
    if verbose_logging:
        GREEN = "\033[32m"
        RESET = "\033[0m"
        print(f"{GREEN}", end="")
        print(*args, **kwargs)
        print(f"{RESET}", end="")
