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

# Taken from https://en.wikipedia.org/wiki/Braille_ASCII
braille_table = {
    "a": "⠁",
    "b": "⠃",
    "c": "⠉",
    "d": "⠙",
    "e": "⠑",
    "f": "⠋",
    "g": "⠛",
    "h": "⠓",
    "i": "⠊",
    "j": "⠚",
    "k": "⠅",
    "l": "⠇",
    "m": "⠍",
    "n": "⠝",
    "o": "⠕",
    "p": "⠏",
    "q": "⠟",
    "r": "⠗",
    "s": "⠎",
    "t": "⠞",
    "u": "⠥",
    "v": "⠧",
    "w": "⠺",
    "x": "⠭",
    "y": "⠽",
    "z": "⠵",
    " ": "⠀",
    "0": "⠴",
    "1": "⠂",
    "2": "⠆",
    "3": "⠒",
    "4": "⠲",
    "5": "⠢",
    "6": "⠖",
    "7": "⠶",
    "8": "⠦",
    "9": "⠔",
    ":": "⠱",
    ";": "⠰",
    "<": "⠣",
    "=": "⠿",
    ">": "⠜",
    "?": "⠹",
    "(": "⠷",
    ")": "⠾",
    "*": "⠡",
    "+": "⠬",
    "-": "⠤"
}

# Convert the provided text to braille, or return an empty string if conversion is not possible
# TODO unit test
def convert(text):
    braille = ""
    if isinstance(text, str):
        lower = text.lower()
        for c in lower:
            if c in braille_table:
                braille = braille + braille_table[c]
    return braille

    