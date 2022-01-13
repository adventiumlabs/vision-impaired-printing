# Copyright 2022 Adventium Labs
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import cv2
import math

def generateScadText(contours, userxmax, userymax, userzheight, resolution):
    print("Scaling to maximum X span " + str(userxmax) + "mm, maximum Y span " + str(userymax) + "mm, resolution " + str(resolution) + "mm, and height " + str(userzheight) + "mm.")
    scad_full_text ="fudge = 0.1;"
    scad_full_text += "\n"

    resolutionScaleFactor = 1
    if resolution is not None:
        # Resolution is in px per inch
        # we need px per mm
        pxPerMm = resolution / 25.4
        resolutionScaleFactor = 1/pxPerMm

    maxX = 0
    minX = 0
    maxY = 0
    minY = 0
    for contour in contours:
        approx_poly = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True),True)
        for pnt in approx_poly:
            if pnt[0][0] > maxX:
                maxX = pnt[0][0]
            if pnt[0][0] < minX:
                minX = pnt[0][0]
            if pnt[0][1] > maxY:
                maxY = pnt[0][1]
            if pnt[0][1] < minY:
                minY = pnt[0][1]

    xSpan = maxX - minX
    ySpan = maxY - minY

    scaleFactor=1
    xscaleFactor=1
    yscaleFactor=1
    if userxmax is not None:
        if xSpan > userxmax:
            xscaleFactor = userxmax / xSpan
    if userymax is not None:
        if ySpan > userymax:
            yscaleFactor = userymax / ySpan
    
    scaleFactor = min(scaleFactor, xscaleFactor, yscaleFactor, resolutionScaleFactor)
    print("Using scale factor " + '{0:.3g}'.format(scaleFactor) + "mm per pixel")

    if(scaleFactor == xscaleFactor and userxmax is not None):
        print("Scaling model based on -x (--xmax) constraint of " + str(userxmax) + "mm maximum horizontal size.")
    if(scaleFactor == yscaleFactor and userymax is not None):
        print("Scaling model based on -y (--ymax) constraint of " + str(userymax) + "mm maximum horizontal.")
    if(scaleFactor == resolutionScaleFactor and resolution is not None):
        print("Scaling model based on requested resolution (-r, --resolution) of " + str(resolution) + "pixels per inch (" + '{0:.3g}'.format((resolution / 25.4)) + " pixels per mm).")

    xOffset = (xSpan // 2) * scaleFactor
    yOffset = (ySpan // 2) * scaleFactor

    scad_modules = []

    i = 0
    for contour in contours:
        approx_poly = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True),True)

        i += 1
        scad_modulename = "poly_path_" + str(i)
        scad_modules.append(scad_modulename)

        # The approximate polygon can also work for SCAD
        scad_moduletext = "module " + scad_modulename + "(h)"
        scad_moduletext += "\n{"
        scad_moduletext += "\nscale([1,1,1]) union()"
        scad_moduletext += "\n{"
        scad_moduletext += "linear_extrude(height=h)"
        scad_moduletext += "polygon(points=["
        
        first = True
        for pnt in approx_poly:
            xPnt = (pnt[0][0]*scaleFactor)
            xPnt -= xOffset
            yPnt = (-1 * pnt[0][1])*scaleFactor
            yPnt += yOffset
            text = "[" + str(xPnt) + "," + str(yPnt) + "]"
            if first:
                scad_moduletext = scad_moduletext + "\n" + text
                first = False
            else:
                scad_moduletext = scad_moduletext + ",\n" + text

        scad_moduletext = scad_moduletext + "\n]"
        scad_moduletext += ");"
        scad_moduletext += "}"
        scad_moduletext += "}"  
        scad_full_text += "\n" + scad_moduletext

    scad_full_text += "module diagonal_line(h)"
    scad_full_text += "\n{"

    for module in scad_modules:
        scad_full_text += "\n" + module + "(h);"
    scad_full_text += "\n}"

    scad_full_text += "\ndiagonal_line(" + str(userzheight) + ");\n"
    return scad_full_text