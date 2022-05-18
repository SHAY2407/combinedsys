#!/usr/bin/env python3

import dearpygui.dearpygui as dpg
import time
import asyncio


class Ultrasonic:
    """A dearpygui window for taking input for ultrasonic distance sensor and
    graphing the resulting values.
    Requires a valid dpg context to already be created.
    """

    def __init__(self, zmq_ctx, uri, **dpg_window_args):
        """Args:
        zmq_ctx: (zmq.Context): ZeroMQ context to use
        uri: (str, optional): Default ip and port for client
        """
        self.started = False
        self.zmq_ctx = zmq_ctx
        with dpg.window(
            label="Ultrasonic Distance", width=700, height=600, **dpg_window_args
        ):
            self.uri_entry = dpg.add_input_text(
                label="Client IP", default_value=uri, decimal=True
            )
            self.start_btn = dpg.add_button(
                label="Start Stream", callback=self.start_cmd
            )
            self.dist_data, self.time_data = [], []
            with dpg.plot(height=500, width=700, label="Distance"):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                self.plot_y = dpg.add_plot_axis(dpg.mvYAxis, label="y")
                self.plot_series = dpg.add_line_series(
                    self.time_data,  # First X axis
                    self.dist_data,  # Then Y axis
                    label="Distance (in cm)",
                    parent=self.plot_y,
                )

    def _update_series(self, dist, time):
        self.dist_data.append(dist)
        self.time_data.append(time)
        dpg.set_value(self.plot_series, [self.time_data, self.dist_data])

    def start_cmd(self, sender):
        self.uri = dpg.get_value(self.uri_entry)
        print(self.uri)
        self._server_start()

    def _server_start(self):
        self.__ultrasonic = Ultrasonic(self.uri, self.zmq_ctx)
        self.ultrasonic.start()
        self.started = True

    async def update(self):
        dist = await self.ultrasonic.get_distance()
        self._update_series(dist, time.time())


if __name__ == "__main__":
    import zmq
    import socket

    async def test():
        dpg.create_context()
        v = Ultrasonic(zmq.Context(), socket.gethostbyname(socket.gethostname()))

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
