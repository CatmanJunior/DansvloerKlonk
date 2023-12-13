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



