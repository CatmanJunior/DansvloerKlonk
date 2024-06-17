import pygame
import random
from functools import partial
from constants import *
from midi import *
from classes import Tile, Object, ObjectList, ObjectDict
import config
import mqtt
from uiDrawer import draw_tile, draw_active_tile

midi_init()

configer = config.Config()
configer.load_config(unique_sections="MQTT TILES UI".split())
# configer.read("config.ini")
print(dir(configer))

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


# PyGame Setup
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
gameLoop = True

# Sequencer setup
currentBeat = 0
lastTick = 0

def createTileList():
    tile_list = []
    for tile_id in range(1, TOTAL_TILES + 1):
        beat = TILE_ORDER_MAPPING[tile_id-1]
        row = beat % GRID[0]
        col = beat // GRID[0]
        new_tile = Tile(tile_id, row, col, beat)
        new_tile.set_object(ObjectList[0])
        tile_list.append(new_tile)
    return tile_list

tile_list = createTileList()

tileDict = {tile.id: tile for tile in tile_list}

print("Tiles created: " + str(len(tile_list)))
print("Beat each tile is on: " + str([tile.beat for tile in tile_list]))


def empty_all_tiles():
    for tile in tile_list:
        tile.RemoveObject()

def PopulateRandomTile():
    random.choice(tile_list).set_object(random.choice(ObjectList))

def EmptyRandomTile():
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
    pygame.K_SPACE: PopulateRandomTile,
    pygame.K_p: PopulateRandomTile,
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
            draw_tile(tile, window)
            if tile.beat == currentBeat:
                sendMidi(tile.object)
                mqtt.SendTileColor(tile, WHITE)
                if DEBUG:
                    print(str(currentBeat) + ": " + tile.object.name +
                          " on tile " + str(tile.id) + " at beat " + str(tile.beat))
                draw_active_tile(tile,window)
            else:
                mqtt.SendTileColor(tile)

        currentBeat += 1

        pygame.display.flip()

    clock.tick(180)

mqtt.Stop()
pygame.quit()
