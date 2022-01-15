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

from matplotlib.pyplot import plot
import numpy as np
import cv2
import sys
import argparse
import os
import math
import scad_generator

def getDebugColors():
    #https://stackoverflow.com/questions/16658018/channel-order-in-opencv
    # OpenCV uses BGR
    colors = {}
    colors[0] = [(255,0,0), "blue"]
    colors[1] = [(0,255,0), "green"]
    colors[2] = [(0,0,255), "red"]
    colors[3] = [(255,255,0), "teal"]
    colors[4] = [(0, 255, 255), "yellow"]
    colors[5] = [(255,0,255), "purple"]
    colors[6] = [(128, 0,0), "dark blue"]
    colors[7] = [(0, 128, 0), "dark green"]
    colors[8] = [(0,0,128), "dark red"]
    colors[9] = [(128,128,128), "gray"]
    return colors

def main():

    parser = argparse.ArgumentParser(description="Convert a bitmap image to an OpenSCAD Module. " +
    "Input image should have a white background.")
    parser.add_argument('-i', '--infile', dest='inputfile', required=True, help='Input file, png recommended.')
    parser.add_argument('-d', '--debug', dest='debug', required=False, action='store_true', help='Debug flag to generate additional output.')
    parser.add_argument('-s', '--split', dest='desiredsplit', default=5, type=int, required=False, help="Split value to use when dividing the image." +
     "A split of five will cause the image to be split into 25 pieces before generating polygons. If some of the elements in your image " +
     "are masking elements inside of them, try increasing the split value.")
    parser.add_argument('-x', '--xmax', dest='xmax', type=int, required=False, help="Uniformly scale the model to fit a maximum X axis distance.")
    parser.add_argument('-y', '--ymax', dest='ymax', type=int, required=False, help="Uniformly scale the model to fit a maximum Z axis distance.")
    parser.add_argument('-z', '--zheight', dest='zheight', type=int, required=False, default=0.2, help="Height of the model to generate")
    parser.add_argument('-r', '--resolution', dest='resolution', type=int, required=False, help="Resolution of the input image in pixels per inch.")
    args = parser.parse_args()
    input_filename = args.inputfile
    if not os.path.isfile(input_filename):
        print("Input file " + input_filename + " does not exist or is not a file.")
        return 1
    
    print("Parsing image " + input_filename)

    # Make three variations of the input image
    try:
        color_image = cv2.imread(input_filename)
        grayscale_image = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)
        paths_blank_image = np.zeros(color_image.shape, dtype=np.uint8)
    except Exception as e:
        print("Failed to read image from file " + input_filename + " error: " + str(e))
        return 1

    print("Input image dimensions: " + str(color_image.shape))


    colors = getDebugColors()

    goodContours = []

    # A split of 5 means we cut the image into a 5x5 grid
    split = 5

    if args.desiredsplit is not None:
        split = args.desiredsplit

    imageHeight = grayscale_image.shape[0]
    imageWidth = grayscale_image.shape[1]

    print("Image width " + str(imageWidth) + " image height " + str(imageHeight))

    print("Using split " + str(split))


    # // means divide and discard remainder
    maskWidth = imageWidth // split
    maskHeight = imageHeight // split

    # TODO there are going to be cases where this gets weird, may need to pad the input image
    if args.debug:
        print("mask width = " + str(maskWidth) + " mask height = " + str(maskHeight))

    i = 0
    for y in range(0, imageHeight, maskHeight):
        for x in range(0, imageWidth, maskWidth):
            snip = grayscale_image[y:y+maskHeight, x:x+maskWidth]
            base = np.zeros(grayscale_image.shape, np.uint8)
            base[:] = (255)
            base[y:y+maskHeight, x:x+maskWidth] = snip

            if args.debug:
                chunk_file_name = os.path.splitext(input_filename)[0] + "-chunk_" + str(x) + "_" + str(y) + ".png"
                try:
                    success = cv2.imwrite(chunk_file_name, base)
                    print("Wrote reference chunk image for chunk " + str(x) + "_" + str(y) + " to: " + chunk_file_name)
                except Exception as e:
                    print("Failed to write chunk image for chunk " + str(x) + "_" + str(y) + " " + str(e))
            
            # https://www.geeksforgeeks.org/python-detect-polygons-in-an-image-using-opencv/
            _,threshold = cv2.threshold(base, 210, 255, cv2.THRESH_BINARY)
            contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if args.debug:
                print("Using split of " + str(split) + " OpenCV found " + str(len(contours)) + " contours for selection [(" + str(x) + "," + str(y) + "),(" + str(x+maskWidth) + "," + str(y+maskHeight) + ")].")

            for contour in contours:
                # If a contour is a square starting at the origin, it's probably the outline, ignore it. 
                if contour[0][0].all() == 0:
                    continue

                # TODO check for contours on the outside border of the image.

                i += 1

                goodContours.append(contour)

                if args.debug:
                    approx_poly = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True),True)
                    # For debugging, draw this contour on the blank image
                    cv2.drawContours(paths_blank_image, [approx_poly], 0, colors[i%len(colors.keys())][0],1)

    if args.debug:
        contour_path_file_name = os.path.splitext(input_filename)[0] +  "-path.png"
        try:
            success = cv2.imwrite(contour_path_file_name, paths_blank_image)
            print("Wrote reference path image to: " + contour_path_file_name)
        except Exception as e:
            print("Failed to write path image: " + str(e))
    
    # Now write the whole thing to a file
    print("Found " + str(len(goodContours)) + " contours")
    scad_full_text = scad_generator.generateScadText(contours=goodContours, userxmax=args.xmax, userymax=args.ymax, userzheight=args.zheight, resolution=args.resolution)

    scad_file_name = os.path.splitext(input_filename)[0] + ".scad"
    with open(scad_file_name, "w") as text_file:
        text_file.write(scad_full_text)
        print("Generated SCAD file: " + scad_file_name)        

    if args.debug:
        path_file_name = os.path.splitext(input_filename)[0] + "-path.png"
        try:
            success = cv2.imwrite(path_file_name, paths_blank_image)
            print("Wrote reference path image to: " + path_file_name)
        except Exception as e:
            print("Failed to write path image: " + str(e))
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main());