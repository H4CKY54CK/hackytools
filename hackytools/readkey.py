import sys

__all__ = [
    'readkey',
]

if sys.platform == 'win32':
    import msvcrt
    def readkey():
        ch = msvcrt.getch()
        while msvcrt.kbhit():
            ch += msvcrt.getch()
        return ch

else:
    import tty
    import termios


    def _read():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            character = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return character


    def readkey(single=None):
        result = _read()
        if not single and result == '\x1b':
            b = _read()
            result += b
            if b == '[':
                while True:
                    b = _read()
                    result += b
                    if b.isalpha() or b == '~':
                        break
            elif b.isdigit():
                while True:
                    b = _read()
                    result += b
                    if b.isalpha() or b == '~':
                        break
            elif b.isalpha():
                result += _read()
        return result
