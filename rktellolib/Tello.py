from rktellolib.TelloCommand import TelloCommand
from rktellolib.TelloState import TelloState
from rktellolib.TelloCam import TelloCam
from typing import Callable

"""
Class Description:
  Tello is the primary interface to interact with the Tello drone.
  It utilizes the three classes TelloCommand, TelloState, and TelloCam to provide interfaces with the drone.
Public Attributes: None
Public Methods:
  - Operational: connect, disconnect, takeoff, land
  - Discrete action: up, down, left, right, forward, back, cw, ccw
  - RC control: rc
  - Camera: get_frame
  - States:
    - General: get_states, get_state
    - System & Environment: get_battery, get_flight_time, get_temp, get_barometer,
    - Positional: get_height, get_distance_tof, get_ax, get_ay, get_az, get_vx, get_vy, get_vz
    - Rotational: get_roll, get_pitch, get_yaw
"""
class Tello():

  __command = None      # the TelloCommand object to issue commands
  __state = None        # the TelloState object to retrieve state information
  __cam = None          # the TelloCam object to retrieve video streams

  __has_video = False   # boolean flag for using the video stream or not
  __is_flying = False   # boolean flag to determine is the drone is flying or not

  """
  Constructor that instantiates the needed objects
  Argument: state_callback - A Callable that will receive the drone state on a separate thread 
  """
  def __init__(self, debug: bool=False, has_video: bool=False, state_callback: Callable[[str],None]=None):
    self.__has_video = has_video

    self.__command = TelloCommand(debug)
    self.__state = TelloState(debug, state_callback)

    if has_video:
      self.__cam = TelloCam()

  """
  Operational commands
  """
  # Start the services and set the Tello to command mode
  def connect(self):
    self.__command.start()
    self.__state.start()

    if self.__has_video:
      self.__command.send('streamoff')
      self.__command.send('streamon')
      self.__cam.start()

  # Land if flying and stop all services
  def disconnect(self):
    if self.__is_flying:
      self.__command.send('land')

    if self.__has_video:
      self.__command.send('streamoff')
      self.__cam.stop()

    self.__state.stop()
    self.__command.stop()

  # Start flying
  def takeoff(self):
    response = self.__command.send('takeoff')
    if response == 'ok':
      self.__is_flying = True
    return response

  # Land the drone
  def land(self):
    response = self.__command.send('land')
    if response == 'ok':
      self.__is_flying = False
    return response

  # Keep the connection alive (prevent the drone from landing)
  def keep_alive(self):
    self.__command.send('battery?')

  """
  Discrete action commands
  """
  def up(self, distance: int):
    return self.__command.send('up {}'.format(distance))
  def down(self, distance: int):
    return self.__command.send('down {}'.format(distance))
  def left(self, distance: int):
    return self.__command.send('left {}'.format(distance))
  def right(self, distance: int):
    return self.__command.send('right {}'.format(distance))
  def forward(self, distance: int):
    return self.__command.send('forward {}'.format(distance))
  def back(self, distance: int):
    return self.__command.send('back {}'.format(distance))
  def cw(self, degree: int):
    return self.__command.send('cw {}'.format(degree))
  def ccw(self, degree: int):
    return self.__command.send('ccw {}'.format(degree))

  """
  RC control command
  """
  def rc(self, v_lr: int, v_fb: int, v_ud: int, v_yaw: int):
    self.__command.send_rc(v_lr, v_fb, v_ud, v_yaw)

  """
  Get the most recent camera frame (must have set "has_video" to True in the constructor)
  """
  def get_frame(self):
    if self.__has_video:
      return self.__cam.get()
    else:
      return None

  """
  Methods to retrieve the drone state
  """
  # Get all state fields as a single string
  def get_states(self):
    return self.__state.get()

  # Get any state specified by the string 'field'
  def get_state(self, field: str):
    return self.__state.get(field)

  # Get system and environment states
  # TODO: switch get_battery() back to passive and have users call keep_alive() in the future
  def get_battery(self):
    return self.__command.send('battery?') # return self.get_state('bat')
  def get_flight_time(self):
    return self.get_state('time')
  def get_temp(self):
    return (self.get_state('temph') + self.get_state('templ')) / 2
  def get_barometer(self):
    return self.get_state('baro')

  # Get positional state
  def get_height(self):
    return self.get_state('h')
  def get_distance_tof(self):
    return self.get_state('tof')
  def get_ax(self):
    return self.get_state('agx')
  def get_ay(self):
    return self.get_state('agy')
  def get_az(self):
    return self.get_state('agz')
  def get_vx(self):
    return self.get_state('vgx')
  def get_vy(self):
    return self.get_state('vgy')
  def get_vz(self):
    return self.get_state('vgz')

  # Get rotational state
  def get_roll(self):
    return self.get_state('roll')
  def get_pitch(self):
    return self.get_state('pitch')
  def get_yaw(self):
    return self.get_state('yaw')
