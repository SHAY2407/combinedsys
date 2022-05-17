# This is a class file for server side of controlling the sabertooth
# It will include methods for connecting to the client socket,private methods of movement to send commands to the client,gui
# for printing the current status

# Importing zmq for client-server connection and tkinter for gui and keybindings
import zmq
import zmq.asyncio
import asyncio


class Sabertooth:
    """This is a class file for server side of controlling the sabertooth.
    It will include methods for connecting to the client socket,private methods of movement to send commands to the client,gui
    for printing the current status,etc
    """

    def __init__(self, tcp: str, context):
        self.tcp = (
            tcp  # this is the tcp of the client to which the server will connect to.
        )
        self.context = context

        # Starting a new tkinter window and setting the title and size
        # self.window = tk.Tk()
        # self.window.geometry("400x350")
        # self.window.title("Sabertooth")

    def _connect(
        self,
    ):  # This is a private method to connect to the open port of the client
        self.str_socket = self.context.socket(
            zmq.PUB
        )  # Notice that here Subscriber-Publisher concept is used instead of REQ-REP
        self.str_socket.connect(f"tcp://{self.tcp}:2222")

    def start(self):

        # self.label = tk.Label(self.window, text="Empty")
        # self.label.grid(column=2, row=3)

        self._connect()

        # self.window.bind("w", self.forward)
        # self.window.bind("s", self.backward)
        # self.window.bind("a", self.left)
        # self.window.bind("d", self.right)
        # self.window.bind("x", self.stop)

        # self.window.mainloop()

    # Private methods for movement. Here strings are sent to the client in the form of binary
    async def forward(self):
        return await self.str_socket.send(b"w")

    async def backward(self):
        return await self.str_socket.send(b"s")

    async def left(self):
        return await self.str_socket.send(b"a")

    async def right(self):
        return await self.str_socket.send(b"d")

    async def stop(self):
        return await self.str_socket.send(b"x")


# for Testing purpose
if __name__ == "__main__":
    sab = Sabertooth("192.138.0.108", zmq.Context())
    sab.start()
