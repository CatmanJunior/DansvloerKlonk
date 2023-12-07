class Sample:
    def __init__(self, id, name, midi_values, svg, led_color, nfc_address):
        self.id = id  # Unique identifier for the sample
        self.name = name  # Name describing the sound of the sample
        self.midi_values = midi_values  # List of MIDI values associated with the sample
        self.svg = svg  # SVG representation for the sample
        self.led_color = led_color  # Color in hex format for visual representation
        self.nfc_address = nfc_address  # NFC address for identifying the sample

    def play(self):
        """Logic to play the sample."""
        # Implement the playback logic here. This could trigger MIDI output or other audio playback mechanisms.
        # This is a placeholder implementation as the actual playback logic will depend on your specific requirements and setup.
        print(f"Playing {self.name} with MIDI values: {self.midi_values}")


# sampleList = [
#     Sample(id=0, name="---", midi_values=MIDILIST[0], svg="default.svg", led_color=BLACK, nfc_address="address_0"),
#     Sample(id=56, name="poep", midi_values=MIDILIST[8], svg="poep.svg", led_color=BROWN, nfc_address="address_56"),
#     Sample(id=59, name="kip", midi_values=MIDILIST[5], svg="kip.svg", led_color=ORANGE, nfc_address="address_59"),
#     Sample(id=51, name="gitaar", midi_values=MIDILIST[3], svg="gitaar.svg", led_color=LBLUE, nfc_address="address_51"),
#     Sample(id=52, name="bas", midi_values=MIDILIST[10], svg="bas.svg", led_color=PURPLE, nfc_address="address_52"),
#     Sample(id=53, name="brandweer", midi_values=MIDILIST[1], svg="brandweer.svg", led_color=RED, nfc_address="address_53"),
#     Sample(id=54, name="sax", midi_values=MIDILIST[7], svg="sax.svg", led_color=YELLOW, nfc_address="address_54"),
#     Sample(id=55, name="leeuw", midi_values=MIDILIST[4], svg="leeuw.svg", led_color=LBROWN, nfc_address="address_55"),
#     Sample(id=58, name="robot", midi_values=MIDILIST[6], svg="robot.svg", led_color=GREY, nfc_address="address_58"),
#     Sample(id=67, name="donder", midi_values=MIDILIST[2], svg="donder.svg", led_color=BROWN, nfc_address="address_67"),
#     Sample(id=68, name="banaan", midi_values=MIDILIST[0], svg="banaan.svg", led_color=YELLOW, nfc_address="address_68"),
#     Sample(id=69, name="mic", midi_values=MIDILIST[0], svg="mic.svg", led_color=DBLUE, nfc_address="address_69"),
#     Sample(id=60, name="eend", midi_values=MIDILIST[9], svg="eend.svg", led_color=DGREEN, nfc_address="address_60"),
# ]
