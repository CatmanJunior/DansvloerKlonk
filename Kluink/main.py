
import paho.mqtt.client as mqtt
import pygame
import random
from functools import partial
from constants import *
from midi import *
import config
from classes import Tile, Object, ObjectList, ObjectDict

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


def draw_active_tile(tile):
    rect = pygame.Rect(
        tile.row * (TILE_SIZE + GUTTER_SIZE),
        tile.column * (TILE_SIZE + GUTTER_SIZE),
        TILE_SIZE,
        TILE_SIZE
    )
    pygame.draw.rect(window, color_to_tuple(WHITE),
                     rect, ACTIVE_TILE_BORDER_SIZE)


# MQTT-------
# The callback for when the client receives a
# CONNACK response from the server.


def on_connect(client, userdata, flags, rc, prop):
    print("Connected with result code " + str(rc))
    for tile in range(TOTAL_TILES):
        # Subscribe to the tile topics (t0-t15)
        client.subscribe("t" + str(tile))

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    payload = str(msg.payload)[3:-1]
    # Subtopic -> messages are build as a15. a = NFC. s = Sensor.
    subTop = str(msg.payload)[2]
    # if subtopic is s return
    if subTop == "s":
        return
    if DEBUG:
        print("New Message -> Topic: " + msg.topic +
              " | Subtopic: " + subTop + " | Payload: " + payload)
    # seperate the tile number from the topic if topic is "t" + num
    if msg.topic[0] == "t":
        tileNum = int(msg.topic[1:])
    if tileNum in tileDict:
        tile = tileDict[tileNum]
        if subTop == "a":
            payload = int(payload)
            if payload in ObjectDict and payload != 0:
                obj = ObjectDict[payload]
                sendMidi(obj)
                tile_list[tile.id].SetObject(obj)
                print("Tile " + str(tile.id) + " set to " + obj.name)


def SendColor(tile):
    client.publish("led" + str(tile.id), tile.color + "1")


# print(configer.sections())
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # type: ignore
# client = mqtt.Client(configer['MQTT']['clientName'])
client.on_connect = on_connect
client.on_message = on_message
if CONNECT_TO_BROKER:
    # try:
    client.connect(host="192.168.178.40")
    print("Connected to Broker")
    client.loop_start()
    # except:
    #     print("ERROR: Can't connect to MQTT BROKER")

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


for col in range(GRID[1]):
    for row in range(GRID[0]):
        beat = (row + col * GRID[0]) % BEATS
        new_tile = Tile(len(tile_list), row, col, beat)
        new_tile.set_object(ObjectList[0])
        tile_list.append(new_tile)

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
                SendColor(tile)
                if DEBUG:
                    print(str(currentBeat) + ": " + tile.object.name +
                          " on tile " + str(tile.id) + " at beat " + str(tile.beat))
                draw_active_tile(tile)
            else:
                SendColor(tile)

        currentBeat += 1

        pygame.display.flip()

    clock.tick(180)

client.loop_stop()

pygame.quit()
