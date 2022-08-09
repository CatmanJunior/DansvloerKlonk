import paho.mqtt.client as mqtt
import pygame
import random
from functools import partial
from constants import *
from midi import *
import config

midi_init()

configer = config.Config
configer.load_config(unique_sections="MQTT TILES UI".split())
# configer.read("config.ini")
# print(dir(configer))

class Tile():
    def __init__(self, id, row=0, column=0):
        self.id = id
        self.beat = self.id % BEATS
        self.row = row
        self.column = column
        self.color = BLACK
        self.object = ObjectList[0]
        left = WIDTH / 2 - GRID_SIZE[0] / 2 + (TILE_SIZE + GUTTER_SIZE) * row
        top = HEIGHT / 2 - GRID_SIZE[1] / 2 + \
            (TILE_SIZE + GUTTER_SIZE) * column
        self.rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)

    def SendColor(self, rgb):
        # print("sending : " + str(self.id))
        client.publish("led" + str(self.id), str(rgb) + "1")

    def SetColor(self, rgb):
        self.color = rgb
        self.SendColor(rgb)

    def SetObject(self, obj):
        self.object = obj
        self.SetColor(obj.color)

    def RemoveObject(self):
        self.object = ObjectList[0]
        self.SetColor(BLACK)

    def draw(self):
        if self.color == BLACK:
            pygame.draw.rect(window,
                             color_to_tuple(WHITE),
                             self.rect,
                             2)
        else:
            pygame.draw.rect(window,
                             color_to_tuple(self.color),
                             self.rect,
                             TILE_BORDER_SIZE)

    def draw_active(self):
        pygame.draw.rect(window, color_to_tuple(WHITE),
                         self.rect, ACTIVE_TILE_BORDER_SIZE)

class Object():
    def __init__(self, name="---", id=0, color=BLACK,
                 midi=[0], enabled=True):
        self.name = name
        self.id = id
        self.color = color
        self.midi = midi
        self.enabled = enabled

    def sendMidi(self):
        if BOSS_SAMPLER:
            midi_program(random.choice(BOSS_PROGRAMS))
            MidiOn(self.midi[0])
        else:
            MidiOn(random.choice(self.midi))

ObjectList = [
    Object("---", 0, BLACK, MIDILIST[0]),
    Object("poep", 56, BROWN, MIDILIST[8]),
    Object("kip", 59, ORANGE, MIDILIST[5]),
    Object("gitaar", 51, LBLUE, MIDILIST[3]),
    Object("bas", 52, PURPLE, MIDILIST[10]),
    Object("brandweer", 53, RED, MIDILIST[1]),
    Object("sax", 54, YELLOW, MIDILIST[7]),
    Object("leeuw", 55, LBROWN, MIDILIST[4]),
    Object("robot", 58, GREY, MIDILIST[6]),
    Object("donder", 67, BROWN, MIDILIST[2], enabled=False),
    Object("banaan", 68, YELLOW, MIDILIST[0]),
    Object("mic", 69, DBLUE, MIDILIST[0]),
    Object("eend", 60, DGREEN, MIDILIST[9]), ]

# MQTT-------
# The callback for when the client receives a
# CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for tile in range(TOTAL_TILES):
        # Subscribe to the tile topics (t0-t15)
        client.subscribe("t" + str(tile))

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    payload = str(msg.payload)[3:-1]
    # Subtopic -> messages are build as a15. a = NFC. s = Sensor.
    subTop = str(msg.payload)[2]
    if DEBUG:
        print("New Message -> Topic: " + msg.topic +
              " | Subtopic: " + subTop + " | Payload: " + payload)
# Put this in a function plz
    for tile in tile_list:
        if msg.topic == "t" + str(tile.id) and subTop == "a":
                for obj in ObjectList:
                    if payload == str(obj.id) and obj.id != 0:
                        obj.sendMidi()
                        tile_list[tile.id].SetObject(obj)
                        break
# print(configer.sections())
client = mqtt.Client(configer.clientname)
# client = mqtt.Client(configer['MQTT']['clientName'])
client.on_connect = on_connect
client.on_message = on_message
if CONNECT_TO_BROKER:
    # try:
    client.connect(host="192.168.178.40",
                   port=1883,
                   keepalive=180)
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
        tile_list.append(Tile(id=col * GRID[0] + row, row=row, column=col))


def empty_all_tiles():
    for tile in tile_list:
        tile.RemoveObject()


def PopulateTile():
    random.choice(tile_list).SetObject(random.choice(ObjectList))


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


def default_key_unmapped(case):
    if DEBUG:
        print("nothing mapped to this key: " + pygame.key.name(case))


def key_switcher(case):
    return key_dict.get(case, partial(default_key_unmapped, case))


def color_to_tuple(color_const):
    return((int(color_const[:3]), int(color_const[3:6]), int(color_const[6:9])))


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
            tile.draw()

            if tile.beat == currentBeat:
                tile.object.sendMidi()
                tile.SendColor(WHITE)
                if DEBUG:
                    print(str(currentBeat) + ": " + tile.object.name)
                tile.draw_active()
            else:
                tile.SendColor(tile.color)

        currentBeat += 1

        pygame.display.flip()

    clock.tick(180)

client.loop_stop()


pygame.quit()
