# Summary

There are limited tools available to allow vision-impaired people to interpret graphical information like presentation charts, 
schematics, or electrical diagrams. The popularity and low-cost of 3d printers makes printing tactile representations of graphical 
information possible at a reasonable cost. 

This tool chain uses Open Computer Vision (OpenCV) to extract contours from input bitmap images and generate 3d models for a 3d printer.

# Workflow

This is a brief summary of the workflow. See the wiki for more detail. 

1. Create content. Diagrams need to be on a white background. 
1. Convert text in your diagram to braille using a tool like Inkscape.
1. Create a bitmap image of your diagram (PNG preferred).
1. Run bitmap-to-scad ```bitmap-to-scad.sh -i example.png``` to generate a .scad file.
1. Use OpenSCAD to create a .stl file.
1. Use a 3d printer configuration tool like Ultimaker Cura to create a printer-specific model (e.g., gcode file)
1. Print your diagram! 

# Installation

## Install Prerequisities

This toolchain uses:
- Python3
- OpenCV

Install these via

```
pip3 install opencv-python
pip3 install matplotlib
```

## Install

1. Put this directory somewhere on your computer, such as ```/usr/local/bin```
1. Add the install directory to your path by adding the following to your ~/.bash_profile ```export PATH="/usr/local/bin/vision-impaired-printing:$PATH"```

# Legal

Copyright 2022 Adventium Labs
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.