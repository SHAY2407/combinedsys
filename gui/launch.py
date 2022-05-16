#!/usr/bin/env python3

import dearpygui.dearpygui as dpg
import numpy as np
import asyncio
import zmq.asyncio

# No need for a class here
def show_launcher():
    width = dpg.get_viewport_width() * 0.1
    height = dpg.get_viewport_height()
    with dpg.window(
        no_resize=True,
        no_title_bar=True,
        horizontal_scrollbar=False,
        no_close=True,
        width=width,
        height=height,
        autosize=False,
        tag="launcher_window",
    ):
        dpg.add_button(
            label="Camera",
            width=width,
            height=height // 3,
            tag="camera_launch",
            callback=launch,
        )
        dpg.add_button(
            label="Motor",
            width=width,
            height=height // 3,
            tag="motor_launch",
            callback=launch,
        )
        dpg.add_button(
            label="Dist",
            width=width,
            height=height // 3,
            tag="dist_launch",
            callback=launch,
        )


def launch(sender):
    if sender == "camera_launch":
        pass
    elif sender == "motor_launch":
        print("Motor")
        pass
    elif sender == "dist_launch":
        print("Dist")
        pass


def set_font():
    with dpg.font_registry():
        with dpg.font("iosevka-regular.ttf", 20) as main_font:
            dpg.add_font_chars([0x1F4F7])
            dpg.bind_font(main_font)


if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title=__loader__.name, width=600, height=200)
    set_font()
    show_launcher()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("launcher_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
