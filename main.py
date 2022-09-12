from pydantic import BaseModel
import serial
import time
import GPUtil


class Colors(BaseModel):
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    magenta = 5
    cyan = 6
    white = 7
    default = 9


class Board:
    def __init__(self, port: str):
        self.buf = bytearray()
        self.port = serial.Serial(port, 500000)

    def flush(self):
        self.port.write(self.buf)
        self.buf = bytearray()
        self.port.flush()

    def clear(self):
        self.write("\033c")

    def color(self, c: int):
        s = f"\033{c}m"
        self.write(s)

    def color_reset(self):
        c = Colors()
        self.fg(c.white)
        self.bg(c.black)

    def fg(self, c: int):
        if c < 10:
            self.color(30 + c)
        else:
            print(f"Ignoring color {c}")

    def bg(self, c: int):
        if c < 10:
            self.color(40 + c)
        else:
            print(f"Ignoring color {c}")

    def bwrite(self, b: bytearray):
        self.buf += b

    def write(self, s: str):
        self.bwrite(s.encode('ascii'))

    def writeln(self, s: str):
        self.bwrite(s.encode('ascii'))
        self.bwrite(b'\012\015')


class Monitor:
    def __init__(self, port: str):
        self.colors = Colors()
        self.b = Board(port)

    def write_all(self):
        self.b.clear()
        self.b.color_reset()
        self.b.writeln("hello world")
        self.b.writeln("hello world 2")
        self.write_gpu()
        self.b.flush()

    def write_gpu(self):
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            self.b.fg(self.colors.blue)
            self.b.write(f"GPU{gpu.id}")

            self.b.fg(self.colors.green)
            self.b.write(f" {gpu.load}")

            self.b.fg(self.colors.green)
            self.b.write(f" {gpu.memoryUsed}/{gpu.memoryTotal}")


if __name__ == '__main__':
    m = Monitor('COM3')

    while True:
        m.write_all()
        time.sleep(10)
