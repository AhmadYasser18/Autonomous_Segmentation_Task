# Autonomous_Segmentation_Task
### This repository contains an autonomous segmentation task.

The python code takes a text file containing a LIDAR's 180 readings (scan.txt is the file used in this case) and creates a text file named results.txt containing the objects' numbers and positions using the connected components algorithm.

The LIDAR's max range is 20m.

If no object found, LIDAR's reading = 0.

Readings are consecutive differing by 1 degree.



## Things planned to be improved:
1. Connect each point to the adjacent points (4 max, 2 min)
