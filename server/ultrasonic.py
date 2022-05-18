#!/usr/bin/env python3

import zmq
import asyncio


class Ultrasonic:
    def __init__(self, tcp, context):
        self.tcp = tcp
        self.context = context

    def start(self):
        self.socket = self.context(zmq.SUB)
        self.socket.bind(f"tcp://{self.tcp}:7777")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "".encode(encoding="utf8"))

    async def get_distance(self):
        try:
            dist = (await self.socket.recv()).decode("utf8")
        except asyncio.CancelledError:
            raise
        return dist


if __name__ == "__main__":
    import socket

    async def test():
        u = Ultrasonic(
            socket.gethostbyname(socket.gethostname()), zmq.asyncio.Context()
        )
        u.start()
        while True:
            try:
                t = asyncio.create_task(u.get_distance())
                dist = await t
                print(dist)
            except KeyboardInterrupt:
                break

    asyncio.run(test())
