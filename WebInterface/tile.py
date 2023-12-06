class Tile:
    def __init__(self, id, row=0, column=0, color="000000", object_id=0):
        self.id = id
        self.row = row
        self.column = column
        self.color = color  # Using hex color representation
        self.object_id = object_id  # ID reference to an object

    def to_dict(self):
        """Convert tile information to dictionary for easy JSON serialization."""
        return {
            "id": self.id,
            "row": self.row,
            "column": self.column,
            "color": self.color,
            "object_id": self.object_id,
        }

    def update_color(self, new_color):
        """Update the color of the tile."""
        self.color = new_color

    def update_object(self, new_object_id):
        """Update the object associated with the tile."""
        self.object_id = new_object_id

    # You can add more methods as required for your application
