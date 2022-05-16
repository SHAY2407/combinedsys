#!/usr/bin/env python3

import gui.launch
from gui.video import Video
from gui.distance import Ultrasonic
import dearpygui.dearpygui as dpg
import zmq.asyncio
import asyncio
import socket

dpg.create_context()
dpg.create_viewport(title="Combined System", width=1280, height=720)
gui.launch.set_font()

# Create GUI units
zmq_async_ctx = zmq.asyncio.Context()
host_ip = socket.gethostbyname(socket.gethostname())
v = Video(zmq_async_ctx, host_ip, tag="video_window")
d = Ultrasonic(zmq_async_ctx, host_ip, tag="distance_window")
m = Motor(zmq_async_ctx, host_ip, tag="motor_window")
gui_units = {
    "video": "video_window",
    "distance": "distance_window",
    "motor": "motor_window",
}

gui.launch.show_launcher(gui_units)
dpg.setup_dearpygui()
dpg.show_viewport()


async def run_and_update():
    while dpg.is_dearpygui_running():
        if v.started:
            t = asyncio.create_task(v.update())
            await t
        dpg.render_dearpygui_frame()
    dpg.destroy_context()


asyncio.run(run_and_update())
