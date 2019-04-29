# Boarding Simulation

This program will be used to simulate and find the best boarding method for airlines. Please see full post at https://nedhulseman.wordpress.com/2018/06/15/flight-boarding-simulation-solving-problems-without-data/

## Getting Started

For this program there are 3 modules
  1. Main - used as the control panel to run the simulation
  2. Draw - used to draw everything that doesn't move ie. The plane and jet tunnel
  3. Passengers - used to guide each passenger through every decision and eventually to their seats

## Prerequisites

You will need 5 packages to use this script. You will need to down load pygames.
Pygames is used to visualize the simulation

```
### Main
from random import shuffle
from Draw import draw
from Passengers import passengers
import time

### Passengers
import pygame, sys
from pygame.locals import *
from random import shuffle
import math
import time
import pickle

### Draw
import pygame, sys
from pygame.locals import *
```

## Deployment

To run the simulation just make sure that all 3 modules are in the same directory and that your IDE is accessing that directory. 
At the top of the Main module you will find the following variable declarations:

  num_rows = 28
  num_aisles = 6
  boarding_procedures = ['random', 'front_to_back', 'back_to_front']
  num_zones = 4
  num_iterations = 51
  move_speed = 4
  refresh_rate = 0
  
 In order to start the simulations just enter in what values you want for these and then call the main function at the bottom with 
 desired boarding procedure. 


## Authors

@Ned Hulseman 



