import random
import rtmidi  # https://pypi.python.org/pypi/python-rtmidi
import rtmidi.midiconstants
from constants import *

midiOut = rtmidi.MidiOut() # type: ignore

def MidiClock():
    midiOut.send_message([0xF8])
    print("clock")

def MidiOn(midi_note):
    if MIDI_DEBUG:
        print("Playing midi note: " + str(midi_note))
    midiOut.send_message([0x90, midi_note, 120])

def MidiOff(midi_note):
    midiOut.send_message([0x80, midi_note, 0])

def midi_program(program):
    midiOut.send_message([rtmidi.midiconstants.PROGRAM_CHANGE, program])

def midi_init():
    available_ports = midiOut.get_ports()
    if MIDI_DEBUG:
        print("Available ports:")
        print(available_ports)

    if available_ports:
        try:
            midiOut.open_port(MIDI_DEVICE)
        except:
            print("Can't Open Midi Port \n")
            raise

    # Set program to program 5 (user 1) for BOSS_SAMPLER
    if BOSS_SAMPLER:
        midiOut.send_message([rtmidi.midiconstants.PROGRAM_CHANGE, 4])

    if MIDI_DEBUG:
        MidiOn(MIDILIST[1][0])
        
def sendMidi(object):
    if object is None or not object.enabled:
        return
    if BOSS_SAMPLER:
        chosen_midi = random.choice(BOSS_PROGRAMS)
    else:
        chosen_midi = random.choice(object.midi)
    # send midi note on
    MidiOn(chosen_midi)