import time
import socket
from threading import Thread

"""
Class Description:
  TelloCommand is a utility class to send commands to the Tello drone.
Public Attributes: None
Public Methods:
  - start   # start the drone communication
  - stop    # stop the drone communication
  - send    # send a command to the drone
  - send_rc # send an RC command to the drone
"""
class TelloCommand:
  __debug = False            # Print debug output or not

  __IP = '192.168.10.1'      # IP address of the Tello Drone
  __PORT = 8889              # UDP port for drone commands
  __socket = None            # The socket connection with the drone
  __thread = None            # The thread object to control thread execution
  __thread_started = False   # Flag to determine if the thread is running

  __TIMEOUT = 10             # Time (seconds) to wait for a command response
  __COMM_DELAY = 0.1         # Minimum delay between each discrete command
  __RC_DELAY = 0.001         # Minimum delay between each RC command
  __last_command_time = 0    # Time when the last discrete command was issued
  __last_rc_command_time = 0 # Time when the last RC command was issued

  __current_response = None  # String containig the most recent Tello response (or None)

  """
  Constructor that creates the socket connection and the thread to receive responses
  """
  def __init__(self, debug: bool=True):
    self.__debug = debug

    # Open local UDP port for Tello communication
    self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.__socket.bind(('', self.__PORT))

    # Bind the thread to receive responses from the drone
    self.__thread = Thread(target=self.__thread_function, daemon=True)

  """
  Destructor that only closes the socket when the object is deleted because sockets are not thread safe
  """
  def __del__(self):
    self.__socket.close()

  """
  A thread that continuously checks for a response from the drone.
  If there is a response, then it updates self.__current_response with the message.
  """
  def __thread_function(self):
    while self.__thread_started:
      try:
        response, ip = self.__socket.recvfrom(1024)
        if self.__debug:
          print('[TelloCommand]: {}'.format(response))
        self.__current_response = response.decode("utf-8").rstrip("\r\n")
      except (UnicodeDecodeError, socket.error) as err:
        print('[TelloCommand] Error: {}'.format(err))

  """
  Begin drone communication
  """
  def start(self):
    # Set drone in command mode
    self.__socket.sendto('command'.encode('utf-8'), (self.__IP,self.__PORT))

    # Start the receive thread
    self.__thread_started = True
    self.__thread.start()

  """
  Stop drone communication
  """
  def stop(self):
    self.__thread_started = False

  """
  Send a command to the drone
  Argument: a string command based off the TelloSDK
  Return: String response from the drone or None if timed out
  """
  def send(self, command: str):
    # Wait at least __COMM_DELAY between commands
    delay = time.time() - self.__last_command_time
    if delay < self.__COMM_DELAY:
      time.sleep(delay)

    # Reset the current response and send the command to the drone over the socket
    self.__current_response = None
    self.__socket.sendto(command.encode('utf-8'), (self.__IP,self.__PORT))
    if self.__debug is True:
      print('[TelloCommand] Command Sent: {}'.format(command))

    # Every 0.1s, check whether the response was received (in the thread function)
    timestamp = time.time()
    while not self.__current_response:
      if time.time() - timestamp > self.__TIMEOUT:
        print('[TelloCommand] Timeout. Aborting Command: \'{}\''.format(command))
        return None
      time.sleep(0.1)

    # Log the last successful command time
    self.__last_command_time = time.time()

    # Return the response string
    if self.__debug is True:
      print('[TelloCommand] Response Received: {}'.format(self.__current_response))
    return self.__current_response.lower()

  """
  Send an RC command to the drone
  Arguments: four velocities – v_lr (left/right), v_fb (front/back), v_ud (up/down), v_yaw (rotation)
  Return: None
  """
  def send_rc(self, v_lr: int, v_fb: int, v_ud: int, v_yaw: int):
    # Only send if enough time between commands has elapsed
    if time.time() - self.__last_rc_command_time < self.__RC_DELAY:
      return

    # Clamp the values between -100 to 100 (required by the Tello SDK)
    clamp100 = lambda x : max(-100, min(100, x))
    v_lr = clamp100(v_lr)
    v_fb = clamp100(v_fb)
    v_ud = clamp100(v_ud)
    v_yaw = clamp100(v_yaw)

    # Send the command to the drone via the socket
    command = 'rc {} {} {} {}'.format(v_lr, v_fb, v_ud, v_yaw)
    self.__socket.sendto(command.encode('utf-8'), (self.__IP,self.__PORT))

    if self.__debug is True:
      print('[TelloCommand] RC Command Sent: {}'.format(command))
