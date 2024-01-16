from threading import Timer
import time
from types import FunctionType
from typing import Callable, List, Union
from tile import Tile
from sample import Sample

class Sequencer:
    def __init__(self, num_tiles: int, bpm: int, callback: Callable[[str, dict], None] = lambda x, y: None, sample_list: List[Sample] = []):
        self.tiles: List[Tile] = [Tile(id=i) for i in range(num_tiles)]
        self.samples: List[Sample] = sample_list
        self.current_beat: int = 0
        self.bpm: int = bpm
        self.timeLastBeat: float = time.time()
        self.callback: Callable[[str, dict], None] = callback

    def add_sample(self, sample: Sample) -> None:
        self.samples.append(sample)

    def assign_sample_to_tile(self, tile_id: int, sample_id: int) -> None:
        sample = next((s for s in self.samples if s.id == sample_id), None)
        if sample:
            self.callback("assign_sample_to_tile", {"tile_id": tile_id, "sample_id": sample_id})
            self.tiles[tile_id].assign_sample(sample)
        else:
            print("Sample not found with id: ", sample_id)

    def activate_tile(self, tile_id: int) -> None:
        self.tiles[tile_id].activate()

    def deactivate_tile(self, tile_id: int) -> None:
        self.tiles[tile_id].deactivate()

    def toggle_tile_activation(self, tile_id: int) -> None:
        self.tiles[tile_id].toggle_activation()

    def next_beat(self) -> None:
        self.timeLastBeat = time.time()
        # print("next beat")
        self.current_beat = (self.current_beat + 1) % len(self.tiles)
        self.play_current_beat()
        self.callback("beat", {"current_beat" : self.current_beat, "bpm" : self.bpm})

    def set_tile_color(self, tile_id: int, color: str) -> None:
        self.tiles[tile_id].current_color = color
        self.callback("set_tile_color", {"tile_id": tile_id, "color": color})

    def play_current_beat(self) -> None:
        self.tiles[self.current_beat].play()

    def update(self) -> None:
        if (time.time() - self.timeLastBeat) > (60 / self.bpm):
            self.next_beat()

        t = Timer(0.01, self.update)
        t.start()