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

import argparse
import sys
import os
from xml.etree import ElementTree as ET
from braille_text_converter import convert

def main():
    parser = argparse.ArgumentParser(description="Convert text in a .SVG image to Braille.")
    parser.add_argument('-i', '--infile', dest='inputfile', required=True, help='Input file, SVG required.')
    parser.add_argument('-f', '--overwrite', dest='overwrite', required=False, action='store_true', help='Overwrite existing file')
    parser.add_argument('-d', '--debug', dest='debug', required=False, action='store_true', help='Debug flag to generate additional output.')

    args = parser.parse_args()
    input_filename = args.inputfile
    if not os.path.isfile(input_filename):
        print("Input file " + input_filename + " does not exist or is not a file.")
        return 1

    tree = ET.parse(input_filename)
    root = tree.getroot()

    # TODO is there a better way to check for text in the SVG namespace?
    for elem in root.iter(tag='{http://www.w3.org/2000/svg}text'):
        # TODO check if style is already set, if it is update it rather than replace
        if elem.text is not None:
            if args.debug:
                print("Found text with text " + elem.text)
            elem.text = convert(elem.text)
            elem.set("style", "font-family:'Courier New'")
        tspans = elem.findall('{http://www.w3.org/2000/svg}tspan')
        for tspan in tspans:
            if args.debug:
                print("found tspan with text " + tspan.text)
            tspan.text = convert(tspan.text)
            tspan.set("style", "font-family:'Courier New'")
    
    output_filename = os.path.splitext(input_filename)[0] + "-braille.svg"
    if args.overwrite:
        output_filename = input_filename
    else:
        i = 0
        while os.path.isfile(output_filename):
            i += 1
            output_filename = os.path.splitext(input_filename)[0] + "-" + str(i) + "-braille.svg"
    
    if args.debug:
        print("Writing output file to " + output_filename)
    tree.write(output_filename)

if __name__ == '__main__':
    sys.exit(main());