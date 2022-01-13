# Summary

This tool chain uses Open Computer Vision (OpenCV) to extract contours from input images and generate 3d models. 

# Installation

This uses:
- Python3
- OpenCV

@tsmith installed via

```
pip3 install opencv-python
pip3 install matplotlib
```


You may also have to install scikit-python 

# Using with SimScape

I find that 24pt Courier New works best for generating Braille with Inkscape. 

1. Select all items in SimScape model
1. Right Click -> Format -> Font Style for Selection...
1. Courier New, 24pt
1. Export the image as SVG via the Matlab shell
   1. For a project called `symbols.slx`
   1. `>> print('-ssymbols','-dsvg','symbols.svg')` 
1. Open the image in InkScape
1. Extensions -> Text -> Convert to Braille
1. Export to PNG at 600dpi


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