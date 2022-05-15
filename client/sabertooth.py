# This is a class file for client side of controlling the sabertooth 
# It will include methods for starting the connection between the motor driver and the server and also private methods for directions

# Importing pyserial for serial communication.zmq for client-server communication,numpy for unicode
import serial
import zmq
import numpy as np

class Sabertooth:
    """This is a class file for client side of controlling the sabertooth.
       It will include methods for starting the connection between the motor driver and the server and also private methods for directions
    """


    def __init__(self, USBport: str,tcp: str, baudrate, context):
        # super().__init__()
        self.port = USBport # This is the port for the port which is connected to the motor driver
        self.tcp = tcp      # This the tcp of the the client since client is the reciever here    
        self.baudrate = baudrate  #tThe baudrate of the motor driver(default: 9600)
        self.context = context     
    
    # private method for binding the port on the client 
    def _bind(self): 
        self.str_socket = self.context.socket(zmq.SUB) 
        self.str_socket.bind('tcp://' + self.tcp + ':2222')    # binding the tcp of the server
        self.str_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    
    def start(self):
        # This connects the client to the sabertooth
        self.ser = serial.Serial(port= self.port, baudrate=self.baudrate, bytesize=serial.EIGHTBITS)

        self._bind() # calling the bind method to bind the client to the server


    # These are methods for directing the motor
    def _forward(self):
        self.ser.write(b'\x7f')     # motor 1 : input= 127(forward) 
        self.ser.write(b'\xff')     # motor 2 : input= 255(forward)
    
    def _backward(self):
        self.ser.write(b'\x01')     # motor 1 : input= 1(backward) 
        self.ser.write(b'\x80')     # motor 2 ; input= 128(backward)

    def _right(self):
        self.ser.write(b'\x01')     # motot 1 : input= 1(backward)
        self.ser.write(b'\xff')     # motor 2 : input= 255(forward)

    def _left(self):
        self.ser.write(b'\x7f')     # motor 1 : input= 127(forward)
        self.ser.write(b'\x80')     # motor 2 : input= 128(backward)
    
    def _stop(self):                # both motor stop : input= 0 
        self.ser.write(b'\x00')
    
    # This method is for receiving the signal from the server. It loops the recv() method of zmq and the calls the required function 
    def output(self):   
        while True:
            try:
                command = self.str_socket.recv()
                match command:
                    case b'w':
                        self._forward()
                    case b's':
                        self._backward()
                    case b'a':
                        self._left()
                    case b'd':
                        self._right()
                    case b'x':
                        self._stop()
            except KeyboardInterrupt:
                self.ser.close()
                break

if __name__ == "__main__": 
    sab = Sabertooth("/dev/ttyUSB0",'192.168.0.108',9600,zmq.Context())
    sab.start()
    sab.output()
