Certainly! Here's the updated table for the `Sample` class, reflecting that the `midi_values` attribute can hold multiple MIDI values.

| Attribute           | Type                  | Description                                                                                       | Example Usage                                      |
|---------------------|-----------------------|---------------------------------------------------------------------------------------------------|----------------------------------------------------|
| `id`                | Integer               | A unique identifier for the sample.                                                               | `sample.id = 1`                                    |
| `name`              | String                | The name of the sample, which can describe the sound it represents.                               | `sample.name = "Kick"`                             |
| `midi_values`       | List of Integers      | A list of MIDI values associated with the sample for playing different sounds.                    | `sample.midi_values = [60, 61]`                    |
| `svg`               | String                | An SVG representation for the sample. It can be a filename or SVG content.                         | `sample.svg = "kick.svg"`                          |
| `led_color`         | String                | The color represented in hex format, used for LED displays or visual representation in UI.        | `sample.led_color = "ff0000"`                      |
| `nfc_address`       | String                | NFC address for the sample, used for identifying the sample via NFC technology.                   | `sample.nfc_address = "01"`                        |
| `play()`            | Method                | Logic to play the sample. This might trigger MIDI output or other audio playback mechanisms.      | `sample.play()`                                    |

In this version, `midi_values` is a list of integers, allowing each sample to have multiple MIDI values associated with it. This allows for greater versatility in how each sample can be represented and played, as it can trigger different sounds or a combination of sounds. The `play()` method would need to be implemented to handle this list appropriately, potentially playing multiple MIDI notes or cycling through them based on the specific application logic.

Here's a table describing the `Tile` class, including its attributes, methods, and how it interacts with the `Sample` class:

| Attribute/Method          | Type              | Description                                                                                           | Example Usage                              |
|---------------------------|-------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------|
| `id`                      | Integer           | A unique identifier for the tile, typically representing its position in the sequencer.               | `tile.id = 0`                              |
| `sample`                  | Sample Object     | A `Sample` object assigned to the tile. This represents the sound that will be played on this beat.   | `tile.sample = sample`                     |
| `is_active`               | Boolean           | Indicates whether the tile is active (i.e., whether it should play its sound on this beat).           | `tile.is_active = True`                    |
| `current_color`           | String            | The current color of the tile, which can be used for visual representation in a UI.                    | `tile.current_color = "ff0000"`            |
| `assign_sample(sample)`   | Method            | Assigns a `Sample` object to the tile. It also updates the tile's color based on the sample's LED color. | `tile.assign_sample(sample)`              |
| `activate()`              | Method            | Activates the tile, enabling it to play its assigned sample during the sequencer's cycle.              | `tile.activate()`                          |
| `deactivate()`            | Method            | Deactivates the tile, preventing it from playing its assigned sample.                                  | `tile.deactivate()`                        |
| `toggle_activation()`     | Method            | Toggles the tile's active state. If the tile is active, it becomes inactive, and vice versa.           | `tile.toggle_activation()`                 |
| `play()`                  | Method            | Plays the tile's assigned sample if the tile is active.                                                | `tile.play()`                              |

This table provides an overview of how the `Tile` class is structured and its interaction with the `Sample` class. Each tile can hold a sample, and its playback and visual representation can be controlled through various methods. The `assign_sample()` method not only assigns a sample to the tile but also updates the tile's current color to match the sample's LED color, enhancing the visual aspect of the sequencer. The `play()` method is used to trigger the sample's playback when the sequencer reaches this tile. The `activate()`, `deactivate()`, and `toggle_activation()` methods provide control over whether the tile is active in the sequencer's cycle.

Creating a new `Sequencer` class that can handle all aspects related to `Tile` and `Sample` requires integrating various functionalities like managing a sequence of beats, assigning samples to tiles, and controlling the playback. Here's an outline of how the `Sequencer` class could be structured, along with a description table for its attributes and methods:

### Sequencer Class

```python
class Sequencer:
    def __init__(self, num_beats, bpm):
        self.tiles = [Tile(id=i) for i in range(num_beats)]
        self.samples = []
        self.current_beat = 0
        self.bpm = bpm

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
        self.current_beat = (self.current_beat + 1) % len(self.tiles)
        self.play_current_beat()

    def play_current_beat(self):
        self.tiles[self.current_beat].play()

    # Additional methods as needed...
```

### Sequencer Class Description Table

| Attribute/Method                | Type              | Description                                                                                       | Example Usage                                   |
|---------------------------------|-------------------|---------------------------------------------------------------------------------------------------|-------------------------------------------------|
| `tiles`                         | List of Tile Objects | A list of `Tile` objects, each representing a beat in the sequencer.                            | `sequencer.tiles`                                |
| `samples`                       | List of Sample Objects | A list of `Sample` objects available for assignment to tiles.                                  | `sequencer.samples`                              |
| `current_beat`                  | Integer           | The index of the current beat in the sequencer.                                                   | `sequencer.current_beat`                         |
| `bpm`                           | Integer           | Beats per minute, determining the tempo of the sequencer.                                         | `sequencer.bpm = 120`                            |
| `add_sample(sample)`            | Method            | Adds a `Sample` object to the sequencer's sample list.                                           | `sequencer.add_sample(sample)`                   |
| `assign_sample_to_tile(tile_id, sample_id)` | Method | Assigns a `Sample` to a specific `Tile` by their IDs.                                           | `sequencer.assign_sample_to_tile(0, 1)`          |
| `activate_tile(tile_id)`        | Method            | Activates a tile by its ID, enabling it to play its sample during the sequencer's cycle.          | `sequencer.activate_tile(0)`                     |
| `deactivate_tile(tile_id)`      | Method            | Deactivates a tile by its ID, preventing it from playing its sample.                             | `sequencer.deactivate_tile(0)`                   |
| `toggle_tile_activation(tile_id)` | Method          | Toggles the active state of a tile by its ID.                                                    | `sequencer.toggle_tile_activation(0)`            |
| `next_beat()`                   | Method            | Advances the sequencer to the next beat and triggers playback if the tile is active.              | `sequencer.next_beat()`                          |
| `play_current_beat()`           | Method            | Plays the sample assigned to the current beat's tile, if it is active.                           | `sequencer.play_current_beat()`                  |

This `Sequencer` class manages the sequence of tiles, handles the assignment and activation of samples on tiles, and controls the playback. The `next_beat()` method is particularly important as it advances the sequencer and triggers the sample playback for the active tiles. The `add_sample()`, `assign_sample_to_tile()`, `activate_tile()`, `deactivate_tile()`, and `toggle_tile_activation()` methods provide the necessary functionality to control the state and behavior of the sequencer.

# Real-Life Dance Floor Control System Flowchart

## Frontend (User Interface)
- **User Interaction**
  - Activates/deactivates tiles
  - Changes BPM
  - Other controls

- **Displaying Sequencer State**
  - Shows current state of the sequencer

- **Sending Commands to Backend**
  - Uses API calls/WebSocket messages

- **Receiving Real-time Updates**
  - Updates UI based on backend data

## Backend (Sequencer Logic)
- **Sequencer Control**
  - Manages timing and state of sequencer

- **Sample Management**
  - Handles loading and storing of samples

- **Tile Management**
  - Tracks each tile's state and sample assignment

- **Real-time Communication**
  - Uses WebSockets/MQTT for updates

- **API Endpoints**
  - Provides endpoints for frontend commands

- **Hardware Interface**
  - Interfaces with physical dance floor components

## Flow of Operations
1. **User Interacts with Frontend**
   - User actions are processed.

2. **Frontend Sends Commands to Backend**
   - Via API calls or WebSocket messages.

3. **Backend Processes Commands and Updates State**
   - Sequencer logic and hardware control.

4. **Backend Sends Real-time Updates to Frontend**
   - Using WebSockets/MQTT.

5. **Frontend Updates UI**
   - Reflects changes in sequencer and dance floor state.
