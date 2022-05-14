#!/usr/bin/env python3

import dearpygui.dearpygui as dpg
from server.camera import Camera


class Video:
    """A dearpygui window for taking input for live camera feed.
    Requires a valid dpg context to already be created.
    """

    def __init__(self, zmq_ctx, uri):
        """Args:
        zmq_ctx: (zmq.Context): ZeroMQ context to use
        uri: (str, optional): Default ip and port for client video feed
        """
        self.zmq_ctx = zmq_ctx
        with dpg.window(label="Live VideoFeed", width=500, height=100):
            self.uri_entry = dpg.add_input_text(
                label="Client IP", default_value=uri, decimal=True
            )
            self.start_btn = dpg.add_button(
                label="Start Stream", callback=self.start_cmd
            )

    def start_cmd(self, sender):
        self.uri = dpg.get_value(self.uri_entry)
        print(self.uri)
        self._server_start()

    def _server_start(self):
        self.__camera = Camera("Camera", self.uri, self.zmq_ctx)
        self.__camera.start()


if __name__ == "__main__":
    import zmq

    dpg.create_context()
    v = Video(zmq.Context(), "0.0.0.0:9000")
    dpg.create_viewport(title=__loader__.name, width=600, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
