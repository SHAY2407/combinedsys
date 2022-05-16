#!/usr/bin/env python3

import dearpygui.dearpygui as dpg
from server.camera import Camera
import numpy as np
import asyncio
import zmq.asyncio


class Video:
    """A dearpygui window for taking input for live camera feed.
    Requires a valid dpg context to already be created.
    """

    def __init__(self, zmq_ctx, uri, tag, res=(640, 480)):
        """Args:
        zmq_ctx: (zmq.Context): ZeroMQ context to use
        uri: (str, optional): Default ip and port for client video feed
        """
        self.started = False
        self.zmq_ctx = zmq_ctx
        with dpg.window(
            label="Live VideoFeed",
            width=max(500, res[0]) * 1.10,
            height=max(100, res[1]) * 1.30,
            tag=tag,
        ):
            self.uri_entry = dpg.add_input_text(
                label="Client IP", default_value=uri, decimal=True
            )
            self.start_btn = dpg.add_button(
                label="Start Stream", callback=self.start_cmd
            )
            self.fb = [0] * (res[0] * res[1])
            with dpg.texture_registry(show=False):
                self.raw_texture = dpg.add_raw_texture(
                    res[0], res[1], self.fb, format=dpg.mvFormat_Float_rgb
                )
            dpg.add_image(self.raw_texture)

    def start_cmd(self, sender):
        """This method should only be called once, calling again will result
        in a zmq Address in Use error
        """
        self.uri = dpg.get_value(self.uri_entry)
        print(self.uri)
        self.started = True
        self._server_start()

    async def update(self):
        frame = await self.__camera.get_frame()
        frame = np.flip(frame, 2).ravel()  # Convert from BGR to RGB
        frame = np.asfarray(
            frame, dtype="f"
        )  # Image is displayed on the GPU, so need to convert to float
        frame = np.true_divide(frame, 255.0)  # 32 bit floats
        dpg.set_value(self.raw_texture, frame)

    def _server_start(self):
        self.__camera = Camera("Camera", self.uri, self.zmq_ctx)
        self.__camera.start()


if __name__ == "__main__":
    import zmq
    import socket

    async def test():
        dpg.create_context()
        v = Video(zmq.asyncio.Context(), socket.gethostbyname(socket.gethostname()))
        dpg.create_viewport(title=__loader__.name, width=800, height=800)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            if v.started:
                t = asyncio.create_task(v.update())
                await t
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    asyncio.run(test())
