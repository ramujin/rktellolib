import time
import socket
from threading import Thread

"""
Class Description:
  TelloCommand is a utility class to receive state information from the Tello drone.
Public Attributes: None
Public Methods:
  - start # start the drone communication
  - stop  # stop the drone communication
  - get   # get the state from the drone
"""
class TelloState:
  __debug = False          # Print debug output or not

  __IP = '192.168.10.1'    # IP address of the Tello Drone
  __PORT = 8890            # UDP port for drone state
  __socket = None          # The socket connection with the drone
  __thread = None          # The thread object to control thread execution
  __thread_started = False # Flag to determine if the thread is running

  __current_state = None   # String containing the most recent Tello state response (or None)

  """
  Constructor that creates the thread to receive responses
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
  A thread that continuously checks for a response from the drone every 0.1s.
  If there is a response, then it updates self.__current_state with the message.
  """
  def __thread_function(self):
    while self.__thread_started:
      time.sleep(0.1)
      try:
        state, ip = self.__socket.recvfrom(1024)
        if self.__debug:
          print('[TelloState]: {}'.format(state))
        self.__current_state = state.decode("utf-8").rstrip("\r\n")
      except (UnicodeDecodeError, socket.error) as err:
        print('[TelloState] Error: {}'.format(err))

  """
  Internal method for retrieving a particular state field from the current state
  """
  def __get_state_field(self, name: str):
    for field in self.__current_state.split(';'):
      parts = field.split(':')
      if name == parts[0]:
        return parts[1]
    return None

  """
  Begin drone communication
  """
  def start(self):
    self.__thread_started = True
    self.__thread.start()

  """
  Stop drone communication
  """
  def stop(self):
    self.__thread_started = False

  """
  Get the drone state
  Argument: if a field is supplied, retrieve only that specific value
  Return: String containing the requested state
  """
  def get(self, field:str = None):
    if field is None:
      return self.__current_state
    else:
      return self.__get_state_field(field)
