verbose_logging = True

def vprint(*args, **kwargs):
    if verbose_logging:
        YELLOW = "\033[33m"
        RESET = "\033[0m"
        print(f"{YELLOW}", end="")
        print(*args, **kwargs)
        print(f"{RESET}", end="")
