import base64
import cv2
import zmq

class Camera():
    """
    This is a class used to capture and send image to the server.
    It starts by:
    - Connecting to the socket
    - get the frame and resize it
    - close the frame
    - send the frame to the server
    """

    def __init__(self, context):
        self.context = context
        self.footage_socket = self.context.socket(zmq.PUB)
        self.footage_socket.connect('tcp://10.4.231.124:5555')

    def start(self, index=0):
        self.camera = cv2.VideoCapture(index)  # init the camera

    def get_frame(self):
        self.grabbed, frame = self.camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        return frame
        
    def close(self):
        self.camera.release()

    def send_frame(self,frame):
        self.__setattr__encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        self.footage_socket.send(jpg_as_text)

if __name__ == "__main__":
    ctx = zmq.Context()
    c = Camera(ctx)
    c.start()
    c.close()