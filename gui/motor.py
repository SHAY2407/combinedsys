#!/usr/bin/env python3

import dearpygui.dearpygui as dpg
from server.sabertooth import Sabertooth
import numpy as np
import asyncio
import zmq.asyncio


class Motor:
    def __init__(self, zmq_ctx, uri, **dpg_window_args):
        self.started = False
        self.uri = uri
        self.zmq_ctx = zmq_ctx
        with dpg.window(
            label="Motor Control", width=500, height=150, **dpg_window_args
        ):
            self.uri_entry = dpg.add_input_text(
                label="Client IP", default_value=uri, decimal=True
            )
            self.start_btn = dpg.add_button(label="Connect", callback=self.start_cmd)
            self.task = None
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Forward [W]", callback=self.move_command, tag="w_button"
                )
                dpg.add_button(
                    label="Backward [S]", callback=self.move_command, tag="s_button"
                )
                dpg.add_button(
                    label="Left [A]", callback=self.move_command, tag="a_button"
                )
                dpg.add_button(
                    label="Right [D]", callback=self.move_command, tag="d_button"
                )
                dpg.add_button(
                    label="Stop [B]", callback=self.move_command, tag="b_button"
                )

    async def update(self):
        t = self.task
        self.task = None
        await t

    def start_cmd(self, sender):
        self.sabertooth = Sabertooth(self.uri, self.zmq_ctx)
        self.sabertooth.start()

    def move_command(self, sender):
        if sender == "w_button":
            self.task = self.sabertooth.forward()
        elif sender == "s_button":
            self.task = self.sabertooth.backward()
        elif sender == "a_button":
            self.task = self.sabertooth.left()
        elif sender == "d_button":
            self.task = self.sabertooth.right()
        elif sender == "b_button":
            self.task = self.sabertooth.stop()
