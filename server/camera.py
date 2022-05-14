# This is a class file for server side of the camera.
# It will include methods for starting the camera on the client side ,display a window, take a snapshot, etc

# importing cv2 for videocapture,zmq for port bind, numpy for unicode and base64 for encoding/decoding
import cv2
import zmq
import zmq.asyncio
import asyncio
import base64
import numpy as np


class Camera:

    """This is a class file for server side of the camera.
    It will include methods for starting the camera on the client side ,display a window, take a snapshot, etc
    """

    def __init__(self, name: str, tcp: str, context):
        self.name = name
        self.tcp = tcp
        self.context = context

    # private method for binding the port
    def _bind(self):
        self.footage_socket = self.context.socket(zmq.SUB)
        self.footage_socket.bind(
            "tcp://" + self.tcp + ":5555"
        )  # binding the tcp of the server
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(""))

    # start() will start a window for displaying the camera feed from the client
    def start(self):
        self._bind()  # called the bind method to bind

    async def get_frame(self):
        try:
            frame = (await self.footage_socket.recv()).decode(
                "utf8"
            )  # convert incoming frames from bytes to utf8 strings
            img = base64.b64decode(frame)  # decodin the jpg_text
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)

            # starting a window
            # cv2.imshow(self.name, source)
            # cv2.waitKey(1)

        except asyncio.CancelledError:  # on keyboard interrupt destroy all windows and exit the loop
            raise
        return source


if __name__ == "__main__":
    import socket

    async def test():
        # Camera is opened on the server's ip, NOT the client's ip
        c = Camera(
            "Camera", socket.gethostbyname(socket.gethostname()), zmq.asyncio.Context()
        )
        c.start()
        while True:
            t = asyncio.create_task(c.get_frame())
            img = await t
            cv2.imshow(c.name, img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

    try:
        asyncio.run(test())
    finally:
        cv2.destroyAllWindows()
