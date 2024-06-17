import pygame
from constants import *

# Pygame functions
def draw_tile(tile, window):
    rect = pygame.Rect(
        tile.row * (TILE_SIZE + GUTTER_SIZE),
        tile.column * (TILE_SIZE + GUTTER_SIZE),
        TILE_SIZE,
        TILE_SIZE
    )
    if tile.color == BLACK:
        pygame.draw.rect(window, color_to_tuple(WHITE), rect, 2)
    else:
        pygame.draw.rect(window, color_to_tuple(
            tile.color), rect, TILE_BORDER_SIZE)
    
    font = pygame.font.SysFont(None, 24)  # type: ignore # Adjust the font size as needed

    tile_surface = font.render("tile: " + str(tile.id), True, color_to_tuple(WHITE))  # Render the tile ID as text
    center_x = rect.x + (rect.width - tile_surface.get_width()) // 2
    center_y = rect.y + (rect.height - tile_surface.get_height()) // 2

    beat_surface = font.render("beat: " + str(tile.beat), True, color_to_tuple(WHITE))  # Render the beat number as text
    beat_x = rect.x + (rect.width - beat_surface.get_width()) // 2
    beat_y = rect.y + (rect.height - beat_surface.get_height()) // 2 + 30

    object_surface = font.render("object: " + tile.object.name, True, color_to_tuple(WHITE))  # Render the object name as text
    object_x = rect.x + (rect.width - object_surface.get_width()) // 2
    object_y = rect.y + (rect.height - object_surface.get_height()) // 2 + 60

    window.blit(tile_surface, (center_x, center_y))
    window.blit(beat_surface, (beat_x, beat_y))
    window.blit(object_surface, (object_x, object_y))


def draw_active_tile(tile, window):
    rect = pygame.Rect(
        tile.row * (TILE_SIZE + GUTTER_SIZE),
        tile.column * (TILE_SIZE + GUTTER_SIZE),
        TILE_SIZE,
        TILE_SIZE
    )
    pygame.draw.rect(window, color_to_tuple(WHITE),
                     rect, ACTIVE_TILE_BORDER_SIZE)
    
    
def color_to_tuple(color_const):
    return ((int(color_const[:3]), int(color_const[3:6]), int(color_const[6:9])))