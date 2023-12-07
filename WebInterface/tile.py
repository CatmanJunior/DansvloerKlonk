class Tile:
    def __init__(self, id, sample=None):
        self.id = id  # Unique identifier for the tile
        self.sample = sample  # Sample object assigned to the tile
        self.is_active = False  # Indicates whether the tile is active
        self.current_color = "#FFFFFF"  # Default color of the tile
        self.connected = False  # Indicates whether the tile is connected to the server

    def assign_sample(self, sample):
        """Assigns a Sample object to the tile and updates the tile's color."""
        self.sample = sample
        # Assuming the Sample object has an attribute 'led_color' for its color representation
        self.current_color = sample.led_color if sample else "#FFFFFF"

    def activate(self):
        """Activates the tile."""
        self.is_active = True

    def deactivate(self):
        """Deactivates the tile."""
        self.is_active = False

    def toggle_activation(self):
        """Toggles the tile's active state."""
        self.is_active = not self.is_active

    def play(self):
        """Plays the tile's assigned sample if the tile is active."""
        if self.is_active and self.sample:
            self.sample.play()  # Assuming the Sample object has a 'play' method
    
    def onConnect(self):
        """Sets the tile's connected state to True."""
        self.connected = True
    
    def onDisconnect(self):
        """Sets the tile's connected state to False."""
        self.connected = False
    
    
