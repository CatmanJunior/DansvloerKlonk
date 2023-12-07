from threading import Timer
import time
from tile import Tile

class Sequencer:
    def __init__(self, num_tiles : int, bpm : int):
        self.tiles = [Tile(id=i) for i in range(num_tiles)]
        self.samples = []
        self.current_beat = 0
        self.bpm = bpm
        self.timeLastBeat = time.time()
        self.next_beat_callback = lambda x: None
        
    def add_sample(self, sample):
        self.samples.append(sample)

    def assign_sample_to_tile(self, tile_id, sample_id):
        sample = next((s for s in self.samples if s.id == sample_id), None)
        if sample:
            self.tiles[tile_id].assign_sample(sample)

    def activate_tile(self, tile_id):
        self.tiles[tile_id].activate()

    def deactivate_tile(self, tile_id):
        self.tiles[tile_id].deactivate()

    def toggle_tile_activation(self, tile_id):
        self.tiles[tile_id].toggle_activation()

    def next_beat(self):
        self.timeLastBeat = time.time()
        print("next beat")
        self.current_beat = (self.current_beat + 1) % len(self.tiles)
        self.play_current_beat()
        self.next_beat_callback(self.current_beat)

    def play_current_beat(self):
        self.tiles[self.current_beat].play()

    def update(self):
        if (time.time() - self.timeLastBeat) > (60 / self.bpm):
            self.next_beat()
        
        t = Timer(0.01, self.update)
        t.start()
            
    