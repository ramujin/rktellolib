import cv2
import time
from threading import Thread

"""
Class Description:
  TelloCam is a utility class that enables video streaming from the Tello drone.
Public Attributes: None
Public Methods:
  - start # start the video stream capture
  - stop  # stop the video stream capture
  - get   # get the most recent frame from the drone
NOTE: Requires a 'streamon' command sent to the Tello first if using it independently.
"""
class TelloCam:

  __IP = '192.168.10.1'    # IP address of the Tello Drone
  __PORT = 11111           # UDP port for drone video
  __thread = None          # The thread object to control thread execution
  __thread_started = False # Flag to determine if the thread is running

  __cam = None             # OpenCV camera object to retrieve frames from the drone
  __frame = None           # An image containing the most recent frame (or None)
  __FPS = 30               # Attempted framerate at which to retrieve frames from the drone
  __FRAME_DELAY = 1/__FPS  # Minimum delay between each received frame
  __last_frame_time = 0    # Time when the last frame was received

  """
  Constructor that creates the thread to receive responses
  """
  def __init__(self):
    # Bind the thread to receive images from the drone
    self.__thread = Thread(target=self.__thread_function, daemon=True)

  """
  Destructor that only closes the socket when the object is deleted because sockets are not thread safe
  """
  def __del__(self):
    if self.__cam:
      self.__cam.release()

  """
  A thread that continuously checks for a response from the drone.
  If there is a response, then it updates self.__current_response with the message.
  """
  def __thread_function(self):
    while self.__thread_started:
      if time.time() - self.__last_frame_time > self.__FRAME_DELAY:
        success, temp_frame = self.__cam.read()
        if success:
          self.__frame = temp_frame
        else:
          self.stop()

  """
  Begin receiving the video stream
  """
  def start(self):
    # Open a UDP video stream to the Tello drone
    self.__cam = cv2.VideoCapture('udp://{}:{}'.format(self.__IP, self.__PORT))

    success, self.__frame = self.__cam.read()
    if not success or self.__frame is None:
      raise Exception('[TelloCam] Failed to grab video stream.')

    self.__thread_started = True
    self.__thread.start()

  """
  Stop receiving the video stream
  """
  def stop(self):
    self.__thread_started = False

  """
  Get the current video frame from the drone
  """
  def get(self):
    return self.__frame
