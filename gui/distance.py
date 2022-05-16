#!/usr/bin/env python3

import dearpygui.dearpygui as dpg


class Ultrasonic:
    """A dearpygui window for taking input for ultrasonic distance sensor and
    graphing the resulting values.
    Requires a valid dpg context to already be created.
    """

    def __init__(self, zmq_ctx, uri, tag):
        """Args:
        zmq_ctx: (zmq.Context): ZeroMQ context to use
        uri: (str, optional): Default ip and port for client
        """
        with dpg.window(label="Ultrasonic Distance", width=700, height=600, tag=tag):
            self.uri_entry = dpg.add_input_text(
                label="Client IP and Port", default_value=uri, decimal=True
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
        pass


if __name__ == "__main__":
    import zmq
    import socket

    dpg.create_context()
    v = Ultrasonic(zmq.Context(), socket.gethostbyname(socket.gethostname()))
    # Add some values for testing the plot
    v._update_series(10, 1)
    v._update_series(40, 3)
    v._update_series(50, 5)

    dpg.create_viewport(title=__loader__.name, width=800, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
