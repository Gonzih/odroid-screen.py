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
        self.buf = b''
        self.port = serial.Serial(port, 500000)

    def flush(self):
        print(self.buf)
        self.port.write(self.buf)
        self.buf = b''

    def clear(self):
        self.write('\033c')

    def cursor_reset(self):
        self.write('\033[H')

    def color(self, c: int):
        s = f'\033[{c}m'
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

    def bwrite(self, b: bytes):
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
        self.b.cursor_reset()
        self.b.color_reset()

        self.write_gpu()

        self.b.flush()

    def colorify(self, v, max_v=100.0, limit=0.7, good=2, bad=1):
        current = v / max_v
        if current <= limit:
            self.b.fg(good)
        else:
            self.b.fg(bad)

    def write_gpu(self):
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            self.b.fg(self.colors.blue)
            self.b.write(f" GPU{gpu.id} ")
            self.b.color_reset()

            load = gpu.load * 100
            self.colorify(load, max_v=100.0)
            self.b.write(f" {round(load, 0)}% ")
            self.b.color_reset()

            # self.colorify(gpu.temperature, max_v=90.0, limit=0.8)
            self.b.write(f" {gpu.temperature}C ")
            # self.b.color_reset()

            # self.colorify(gpu.memoryUsed, max_v=gpu.memoryTotal, limit=0.8)
            self.b.writeln(f" {gpu.memoryUsed}/{gpu.memoryTotal} MB ")
            # self.b.color_reset()


if __name__ == '__main__':
    m = Monitor('COM3')

    print('Looping')
    while True:
        m.write_all()
        time.sleep(5)
