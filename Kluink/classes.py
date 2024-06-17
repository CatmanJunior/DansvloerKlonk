# classes.py
import random
from typing import Mapping
from constants import *

class Tile:
    def __init__(self, id, row=0, column=0, beat=0):
        self.id = id
        self.beat = beat
        self.row = row
        self.column = column
        self.color = BLACK  # Default to black
        self.object = None  # Will be set to an instance of Object

    def set_color(self, rgb):
        self.color = rgb

    def set_object(self, obj):
        self.object = obj
        self.set_color(obj.color)

    def remove_object(self):
        self.object = None
        self.set_color(BLACK)  # Reset to black

class Object:
    def __init__(self, name="---", id=0, color=BLACK, midi=[0], enabled=True, midi_callback=None):
        self.name = name
        self.id = id
        self.color = color
        self.midi = midi
        self.enabled = enabled

ObjectList = [
    Object("---", 0, BLACK, MIDILIST[0]),
    Object("poep", 56, BROWN, MIDILIST[8]),
    Object("kip", 59, ORANGE, MIDILIST[5]),
    Object("gitaar", 51, LBLUE, MIDILIST[3]),
    Object("bas", 52, PURPLE, MIDILIST[10]),
    Object("brandweer", 53, RED, MIDILIST[1]),
    Object("sax", 54, YELLOW, MIDILIST[7]),
    Object("leeuw", 55, LBROWN, MIDILIST[4]),
    Object("robot", 58, GREY, MIDILIST[6]),
    Object("donder", 67, BROWN, MIDILIST[2], enabled=False),
    Object("banaan", 68, YELLOW, MIDILIST[0]),
    Object("mic", 69, DBLUE, MIDILIST[0]),
    Object("eend", 60, DGREEN, MIDILIST[9]), ]

# a dictionary of all objects with their id as key
ObjectDict = {obj.id: obj for obj in ObjectList}