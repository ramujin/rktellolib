# RKTelloLib

### In light of the many poorly-designed libraries to interact with the DJI (Ryze) Tello drone that either do way more than they should or don't do enough, I have taken the initiative to create this small library. It's a simple interface built upon the official [Tello SDK](https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf) that allows you to control and interact with the drone with minimal effort.


## Installation

### Install using PIP

```bash
$ pip install rktellolib
```

### Install from Source

```bash
$ git clone https://github.com/ramujin/rktellolib.git
$ cd rktellolib
$ pip install -e .
```

## Example Usage to Fly in a Square Pattern

```python
from rktellolib import Tello

drone = Tello(debug=True, has_video=False)

drone.connect()
drone.takeoff()

drone.forward(100)
drone.cw(90)
drone.forward(100)
drone.cw(90)
drone.forward(100)
drone.cw(90)
drone.forward(100)
drone.cw(90)

drone.land()
drone.disconnect()
```

## Example Usage to Stream Video

```python
from rktellolib import Tello
import cv2

drone = Tello(debug=True, has_video=True)

drone.connect()

while True:
  frame = drone.get_frame()
  if frame is None:
    break

  cv2.imshow('rktellolib', frame)

  if cv2.waitKey(1) == 27: # ESC key
    break

drone.disconnect()
```

## Available Commands

```python
# Operational Commands
connect()
disconnect()
takeoff()
land()

# Discrete Action Commands
up(distance: int)
down(distance: int)
left(distance: int)
right(distance: int)
forward(distance: int)
back(distance: int)
cw(degree: int)
ccw(degree: int)

# RC Control Command
rc(v_lr: int, v_fb: int, v_ud: int, v_yaw: int)

# Camera Command
get_frame()

# State Retrieval Commands
# All States
get_state()

# System & Environment States
get_battery()
get_flight_time()
get_temp()
get_barometer()

# Positional States
get_height()
get_distance_tof()
get_ax()
get_ay()
get_az()
get_vx()
get_vy()
get_vz()

# Rotational States
get_roll()
get_pitch()
get_yaw()