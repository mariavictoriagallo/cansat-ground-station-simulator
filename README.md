# CanSat Telemetry Ground Station Simulator
This Python ground station simulator processes real-time telemetry data from a falling satellite (CanSat). Built using tkinter and matplotlib for Code in Place, it prototypes data-parsing, graphical layout, and analytics ahead of developing a physical CanSat for my school final project later this year.

## Project Overview
the application simulates the real-time descent of a satellite after being dropped from a drone. it generates a live radio stream packet containing altitude, temperature, gps, and orientation (imu) updates. the graphical dashboard dynamically parses this text payload, alerts the operator during low altitudes, freezes the sensors at touchdown, and automatically pops up visual data charts using `matplotlib`.

## Project Value
this simulator is incredibly useful because it bridges the gap between hardware telemetry and software display systems. instead of waiting for a physical radio module to be wired and flashed, this program provides a safe environment to design, arrange, and test a mission control interface. the foundational string-splitting and list-tracking logic can easily be transferred to handle live serial data from an actual microcontroller later.

## Getting Started
make sure you have python installed on your system. then, install the external graphing library using your terminal:

pip install matplotlib

## Execution
download the project file and launch the ground station app:

python ground_station.py

## Maintainers
this project is completely designed, written, and maintained by me as a final project milestone for Code in Place (2026). it serves as a software prototype for my upcoming technical school project. feel free to suggest layout updates!
