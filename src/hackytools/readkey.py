import sys

__all__ = [
    'readchar',
    'readkey',
]

if sys.platform == 'win32':
    import msvcrt

    def readchar():
        return msvcrt.getch()

    def readkey():
        key = msvcrt.getch()
        keys = [key]
        while msvcrt.kbhit():
            keys.append(msvcrt.getch())
        return "".join(keys)

else:
    def readchar():
        """Read a single character from sys.stdin and return it."""
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        character = ""
        try:
            tty.setraw(fd)
            character = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return character

    def readkey():
        """Read a full key sequence from sys.stdin and return it."""
        key = []
        key.append(readchar())
        if ord(key[-1]) == 27:
            key.append(readchar())
            while not key[-1].isalpha() and not ord(key[-1]) in (27, 126):
                key.append(readchar())
        return "".join(key)
    # import tty
    # import termios


    # def _read():
    #     fd = sys.stdin.fileno()
    #     old = termios.tcgetattr(fd)
    #     try:
    #         tty.setraw(sys.stdin.fileno())
    #         character = sys.stdin.read(1)
    #     finally:
    #         termios.tcsetattr(fd, termios.TCSADRAIN, old)
    #     return character


    # def readkey(single=False):
    #     key = _read()
    #     keys = [key]
    #     if single is False and ord(key) == 27:
    #         key = _read()
    #         keys.append(key)
    #         if key == '[':
    #             while True:
    #                 key = _read()
    #                 keys.append(key)
    #                 if key.isalpha() or key == '~':
    #                     break
    #         elif key.isdigit():
    #             while True:
    #                 key = _read()
    #                 keys.append(key)
    #                 if key.isalpha() or key == '~':
    #                     break
    #         elif key.isalpha():
    #             key = _read()
    #             keys.append(key)
    #     return "".join(keys)

    # def readkey(single=False):
    #     key = _read()
    #     if not single and ord(key) == 27:
    #         b = _read()
    #         key += b
    #         if b == '[':
    #             while True:
    #                 b = _read()
    #                 key += b
    #                 if b.isalpha() or b == '~':
    #                     break
    #         elif b.isdigit():
    #             while True:
    #                 b = _read()
    #                 key += b
    #                 if b.isalpha() or b == '~':
    #                     break
    #         elif b.isalpha():
    #             key += _read()
    #     return key
