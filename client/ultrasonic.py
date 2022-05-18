#!/usr/bin/env python3

import zmq
import serial


class Ultrasonic:
    def __init__(self, context, uri, **serial_args):
        self.context = context
        self.uri = uri
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(self.uri)
        self.board = serial.Serial(**serial_args)

    def start(self, index=0):
        self.board.open()
        self._bind()

    def get_distance(self):
        return self.board.read_line()

    def send_distance(self, dist):
        self.socket.send(dist)

    def close(self):
        self.board.close()


if __name__ == "__main__":
    ctx = zmq.Context()
    u = Ultrasonic(
        ctx, "tcp://192.168.1.137:7777", port="/dev/ttyUSB0", baudrate=115200
    )
    u.start()
    while True:
        try:
            d = u.get_distance()
            u.send_distance(d)
        except KeyboardInterrupt:
            u.close()
            break
