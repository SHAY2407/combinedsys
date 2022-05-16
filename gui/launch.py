#!/usr/bin/env python3

import dearpygui.dearpygui as dpg
import numpy as np
import asyncio
import zmq.asyncio

# No need for a class here


def show_launcher(gui_units):
    """Draws a sidebar serving as a launcher for other windows.
    Args:
        gui_units: A dictionary containing the objects to launch
    """
    width = dpg.get_viewport_width() * 0.1
    height = dpg.get_viewport_height()
    with dpg.window(
        no_resize=True,
        no_title_bar=True,
        horizontal_scrollbar=False,
        no_close=True,
        width=width,
        height=-1,
        autosize=True,
        tag="launcher_window",
    ):
        dpg.add_button(
            label="Camera",
            width=width,
            height=height // 3,
            tag="camera_launch",
            callback=launch,
            user_data=gui_units,
        )
        dpg.add_button(
            label="Motor",
            width=width,
            height=height // 3,
            tag="motor_launch",
            callback=launch,
            user_data=gui_units,
        )
        dpg.add_button(
            label="Dist",
            width=width,
            height=height // 3,
            tag="dist_launch",
            callback=launch,
            user_data=gui_units,
        )


def launch(sender, value, gui_units):
    if sender == "camera_launch":
        if dpg.is_item_visible(gui_units["video"]):
            dpg.focus_item(gui_units["video"])
        else:
            dpg.show_item(gui_units["video"])
    elif sender == "motor_launch":
        if dpg.is_item_visible(gui_units["motor"]):
            dpg.focus_item(gui_units["motor"])
        else:
            dpg.show_item(gui_units["motor"])
    elif sender == "dist_launch":
        if dpg.is_item_visible(gui_units["distance"]):
            dpg.focus_item(gui_units["distance"])
        else:
            dpg.show_item(gui_units["distance"])


def set_font():
    with dpg.font_registry():
        with dpg.font("iosevka-regular.ttf", 20) as main_font:
            dpg.add_font_chars([0x1F4F7])
            dpg.bind_font(main_font)
