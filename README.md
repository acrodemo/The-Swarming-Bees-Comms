# Drone Simulation
## Overview
This is a simulation to show how the mesh network of our communication system operates in real time. 
Flight plans can be coded in to the system, and you can visually see how data is transferred between each drone.
***
### Icon Guide

<br>


| Object | Description | Image |
| ------ | ----------- | ----- |
| Base Station | Central immobile station <br> first responders will interface <br> with. | <img src="markdownImages/baseStation.png" width="128" style="display: flex;align-items:center;"/> |
| Drone | One of the many drones <br> data will be collected from <br> or transferred to. | <img src="markdownImages/drone.png" width="128" style="display: flex;align-items:center;"/>| 
| Connection | A connection line established <br> by the mesh network through <br> batman-advanced. (Blue lines <br> simply mean the connection is <br> directly to the base station.)| <img src="markdownImages/connection.png" width="128" style="display: flex;align-items:center;"/> | 
| Packet | This represents a packet of <br> information that needs to be<br> transferred back to the base <br> station. | <img src="markdownImages/packet.png" width ="128" style="display: flex; align-items:center;">

<br>

---

## How To Use
Launch droneSim.py. This will open a pygame window. Currently, there is no GUI to assign flight paths. The only inputs implemented are spacebar - which sends a packet from Drone 0, and the arrow keys, which move Drone 0 around. This is purely a proof of concept and a useful demonstration. The code will be built out soon so that it can be used as a more robust system.

There are comments inside of droneSim.py that show where and how to program flight paths or change drone sources. Some python experience is necessary.

#### NOTE:
entities.py and grid.py must be in the same folder as droneSim.py in order for the application to run. 
