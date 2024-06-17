import pygame
import random
from functools import partial
from constants import *
from midi import *
from classes import Tile, Object, ObjectList, ObjectDict
import config
import mqtt

midi_init()

configer = config.Config()
configer.load_config(unique_sections="MQTT TILES UI".split())
# configer.read("config.ini")
print(dir(configer))

def sendMidi(object):
    if object is None or not object.enabled:
        return
    if BOSS_SAMPLER:
        chosen_midi = random.choice(BOSS_PROGRAMS)
    else:
        chosen_midi = random.choice(object.midi)
    # send midi note on
    MidiOn(chosen_midi)

# Pygame functions
def draw_tile(tile):
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


def draw_active_tile(tile):
    rect = pygame.Rect(
        tile.row * (TILE_SIZE + GUTTER_SIZE),
        tile.column * (TILE_SIZE + GUTTER_SIZE),
        TILE_SIZE,
        TILE_SIZE
    )
    pygame.draw.rect(window, color_to_tuple(WHITE),
                     rect, ACTIVE_TILE_BORDER_SIZE)

def on_tile_message(topic, subTopic, payload):
    # seperate the tile number from the topic if topic is "t" + num
    if topic[0] == "t":
        tileNum = int(topic[1:])
    if tileNum in tileDict:
        tile = tileDict[tileNum]
        if subTopic == "a":
            payload = int(payload)
            if payload in ObjectDict and payload != 0:
                obj = ObjectDict[payload]
                sendMidi(obj)
                tile_list[tile.id].set_object(obj)
                print("Tile " + str(tile.id) + " set to " + obj.name)

mqtt.connectToMqtt(msg_Callback=on_tile_message)

tile_list = []
# PyGame Setup
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
gameLoop = True

# Sequencer setup
currentBeat = 0
lastTick = 0


for tile_id in range(1, TOTAL_TILES + 1):
    beat = TILE_ORDER_MAPPING[tile_id-1]
    row = beat % GRID[0]
    col = beat // GRID[0]
    new_tile = Tile(tile_id, row, col, beat)
    new_tile.set_object(ObjectList[0])
    tile_list.append(new_tile)

#order the tiles by beat
# tile_list.sort(key=lambda x: x.beat)

tileDict = {tile.id: tile for tile in tile_list}

print("Tiles created: " + str(len(tile_list)))
print("Beat each tile is on: " + str([tile.beat for tile in tile_list]))


def empty_all_tiles():
    for tile in tile_list:
        tile.RemoveObject()


def PopulateTile():
    random.choice(tile_list).set_object(random.choice(ObjectList))


def EmptyTile():
    random.choice(tile_list).RemoveObject()


def SequencerMode():
    global SEQUENCERMODE
    SEQUENCERMODE = not SEQUENCERMODE
    print("SEQUENCERMODE: " + str(SEQUENCERMODE))


def RandomSequencerMode():
    global RANDOMSEQUENCE
    RANDOMSEQUENCE = not RANDOMSEQUENCE
    print("RANDOMSEQUENCE-Mode: " + str(RANDOMSEQUENCE))


def kill_game():
    global gameLoop
    gameLoop = False


key_dict = {
    pygame.K_SPACE: PopulateTile,
    pygame.K_p: PopulateTile,
    pygame.K_r: empty_all_tiles,
    pygame.K_2: SequencerMode,
    pygame.K_3: RandomSequencerMode,
    pygame.K_ESCAPE: kill_game,
}

# a string containing the name of the keys + function names + /n
key_list = "\n".join([pygame.key.name(key) + " : " +
                     func.__name__ for key, func in key_dict.items()])
print("Keybindings: \n" + key_list)


def default_key_unmapped(case):
    if DEBUG:
        print("nothing mapped to this key: " + pygame.key.name(case))


def key_switcher(case):
    return key_dict.get(case, partial(default_key_unmapped, case))


def color_to_tuple(color_const):
    return ((int(color_const[:3]), int(color_const[3:6]), int(color_const[6:9])))


while gameLoop:
    currentTick = pygame.time.get_ticks()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            keyfunc = key_switcher(event.key)
            keyfunc()
        if (event.type == pygame.QUIT):
            gameLoop = False

    if (currentTick - lastTick >= MILIS_PER_BEAT):
        window.fill(color_to_tuple(BLACK))
        # MidiClock() this need to go every 1/24 of a beat
        # Use thread or something
        # for i in range(24):
        # MidiClock()

        if RANDOMSEQUENCE:
            currentBeat = random.randint(0, BEATS - 1)
        else:

            if (currentBeat >= BEATS):
                currentBeat = 0
                print("---------START AT 0----------")

        lastTick += MILIS_PER_BEAT

        for tile in tile_list:
            draw_tile(tile)
            if tile.beat == currentBeat:
                sendMidi(tile.object)
                mqtt.SendTileColor(tile, WHITE)
                if DEBUG:
                    print(str(currentBeat) + ": " + tile.object.name +
                          " on tile " + str(tile.id) + " at beat " + str(tile.beat))
                draw_active_tile(tile)
            else:
                mqtt.SendTileColor(tile)

        currentBeat += 1

        pygame.display.flip()

    clock.tick(180)

mqtt.Stop()
pygame.quit()
