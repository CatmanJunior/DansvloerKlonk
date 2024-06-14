import paho.mqtt.client as mqtt
import pygame
import random
import rtmidi #https://pypi.python.org/pypi/python-rtmidi

#COLORS
WHITE 	= 	"255255255"
BLACK 	= 	"000000000"
BLUE	=	"000000255"
RED		= 	"255000000"
GREEN	=	"000255000"
PURPLE	=	"255000255"
TURQ	=	"000255255"
YELLOW	=	"255255000"
SKYBLUE	=	"000191255"
VIOLET	=	"238130238"
NEOPINK	=	"255020147"
BROWN	=	"129069019"
ORANGE	=	"255153051"
DGREEN	=	"000102000"
DBLUE	=	"000000153"
LBLUE	=	"153204255"
GREY	=	"100100100"
LBROWN	=	"204102000"

#MQTT Constants
BROKERIP = "192.168.178.40"

#Sequencer Constants
BPM		= 	120		#Beats per Minute
GRID	=	(3,4)	#The layout of the tiles
BEATS	=	12		#The amount of beats to loop 		

TOTALTILES 	= 	GRID[0]*GRID[1]
TPB			=	int(TOTALTILES/BEATS)		#Tiles per beat
MPB         =	1000/(BPM/60)				#Milis per beat

MIDILIST	=	[0,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]
PIANOMIDILIST = [60, 62, 65, 67, 69, 72, 74, 77, 79, 60,62,65, 62, 65, 67, 69, 72, 74, 77, 79, 60,62,65]

def MidiOn(m):
	midiout.send_message([0x90, m, 120])

def MidiOff(m):
	midiout.send_message([0x80, m, 0])

#PYGAME CONSTANTS
TITLE 	= 	"KLONK"
WIDTH 	= 	200
HEIGHT 	= 	200	

#GameModes
MOLEMODE = False
SEQUENCERMODE = True
PIANOMODE = True
RANDOMSEQUENCE = False

#Midi Init
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    midiout.open_port(0)

#TILE CLASS
class Tile():
	def __init__(self, number, beat, row):
		self.id = number
		self.beat = beat
		self.row = row
		self.color = BLACK
		self.MOLEMODE = False
		self.object = ObjectList[0]

	def SendColor(self, rgb):
		client.publish("led" + str(self.id),str(rgb) + "1")

	def LightUp(self, rgb, time):
		pass

	def SetMole(self):
		self.MOLEMODE = True
		self.SetColor(WHITE)

	def SetColor(self, rgb):
		self.color = rgb

	def SetObject(self, obj):
		self.object = obj
		self.SetColor(obj.color)

	def RemoveObject(self):
		self.object = ObjectList[0]
		self.SetColor(BLACK)

#OBJECT CLASS
class Object():
	def __init__(self,name,ide,color,midi):
		self.name = name
		self.id = ide
		self.color = color
		self.midi = midi

	def sendMidi(self):
		MidiOn(self.midi)

ObjectList = []
for i in range(13):
	ObjectList.append(0)

ObjectList[0] = Object("niks", 		0, 		BLACK,	MIDILIST[0])
ObjectList[1] = Object("poep", 		1, 		BROWN,	MIDILIST[1])
ObjectList[2] = Object("kip", 		2, 		ORANGE,	MIDILIST[2])
ObjectList[3] = Object("gitaar", 	3, 		LBLUE,	MIDILIST[3])
ObjectList[4] = Object("bas", 		4, 		PURPLE,	MIDILIST[4])
ObjectList[5] = Object("brandweer", 5, 		RED,	MIDILIST[5])
ObjectList[6] = Object("sax", 		6, 		YELLOW,	MIDILIST[6])
ObjectList[7] = Object("leeuw", 	7, 		LBROWN,	MIDILIST[7])
ObjectList[8] = Object("robot", 	8, 		BLUE,	MIDILIST[8])
ObjectList[9] = Object("donder", 	9, 		DBLUE,	MIDILIST[9])
ObjectList[10] = Object("banaan", 	10, 	YELLOW,	MIDILIST[10])
ObjectList[11] = Object("mic", 		11, 	DBLUE,	MIDILIST[11])
ObjectList[12] = Object("eend", 	12, 	DGREEN,	MIDILIST[12])

#MQTT-------

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, prop):
	print("Connected with result code "+str(rc))
	for i in range(TOTALTILES):
		client.subscribe("t" + str(i)) #Subscribe to the tile topics (t0-t15)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	tempmsg = str(msg.payload)[3:-1]
	#Subtopic -> messages are build as a15. a = NFC. s = Sensor.
	subTop = str(msg.payload)[2] 

	print("New Message -> Topic: " + msg.topic + " | Subtopic: " + subTop + " | Payload: " + tempmsg)
	
	for i in tiles:
		if msg.topic == "t" + str(i.id):
			if subTop == "a":
				for o in ObjectList:
					if tempmsg == str(o.id):
						print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: " + o.name)
						sequencer[i.beat][i.row].SetObject(o)
				if tempmsg == "0":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 0")
					#sequencer[i.beat][i.row] = 0
					#i.SetColor("000000000")
			if subTop == "s":
				if MOLEMODE and i.MOLEMODE:
					i.SetColor("BLACK")
					print("Got the MOLE at -> Tile #" + str(i.id))

				i.SendColor(PURPLE)

				sequencer[i.beat][i.row].RemoveObject()

				if PIANOMODE:
					MidiOn(PIANOMIDILIST[i.id])

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKERIP, port=1883, keepalive=180)
client.loop_start()
	
#PyGame Setup
pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
gameLoop = True

#Sequencer setup
currentBeat = 0;
lastTick = 0
sequencer = []
tiles = []
tileGrid = []
	
for j in range(TPB):
	for i in range(BEATS):
		tiles.append(Tile(j*BEATS+i,i,j))

def SetupSequencer():
	global sequencer, tileGrid
	sequencer = []
	tileGrid = []
	
	for i in range(GRID[0]):
		tileGrid.append([])
		for j in range(GRID[1]):
			tileGrid[i].append(tiles[j+i*GRID[1]])

	for i in range(BEATS):
		sequencer.append([])
		for j in range(TPB):
			sequencer[i].append(tiles[j*BEATS+i])

def EmptyTiles():
	for i in tiles:
		i.RemoveObject()

def PopulateTile():
	a = random.choice(tiles)
	a.SetObject(random.choice(ObjectList))
	
def EmptyTile():
	random.choice(tiles).RemoveObject()
	
def PianoMode():
	global PIANOMODE
	PIANOMODE = not PIANOMODE
	print("PIANOMODE: " + str(PIANOMODE))

def SequencerMode():
	global SEQUENCERMODE
	SEQUENCERMODE = not SEQUENCERMODE
	print("SEQUENCERMODE: " + str(SEQUENCERMODE))

def RandomSequencerMode():
	global RANDOMSEQUENCE
	RANDOMSEQUENCE = not RANDOMSEQUENCE
	print ("RANDOMSEQUENCE: " + str(RANDOMSEQUENCE))

def FakePiano():
	a = random.choice(tiles)
	client.publish("t" + str(a.id),"s50")

SetupSequencer()
print (sequencer)
while gameLoop:
	currentTick = pygame.time.get_ticks()
	
	for event in pygame.event.get():
		if (event.type==pygame.QUIT):
			gameLoop = False
			client.loop_stop()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pass
			if event.key == pygame.K_RIGHT:
				pass
			if event.key == pygame.K_SPACE:
				PopulateTile()
			if event.key == pygame.K_SLASH:
				FakePiano()
			if event.key == pygame.K_p:
				PopulateTile()
			if event.key == pygame.K_r:
				EmptyTiles()
			if event.key == pygame.K_d:
				EmptyTile()
			if event.key == pygame.K_2:
				PianoMode()
			if event.key == pygame.K_1:
				SequencerMode()
			if event.key == pygame.K_3:
				RandomSequencerMode()

	if (currentTick - lastTick >= MPB):

		for i in MIDILIST:
			MidiOff(i)

		if RANDOMSEQUENCE:
			currentBeat = random.randint(0,BEATS-1)
		else:
			currentBeat+= 1;
			if (currentBeat >= BEATS): 
					currentBeat = 0
					print()
			
		lastTick = currentTick

		for i in tiles:
			if i.beat != currentBeat:
				i.SendColor(i.color)

		if MOLEMODE:
			newmole = random.randint(0,len(tiles)-1)
			tiles[newmole].SetMole() 
			print("New Mole = " + str(newmole))
		
		if SEQUENCERMODE:
			for i in range(TPB):
				if (sequencer[currentBeat][i].object != ObjectList[0]):
					print(str(currentBeat) + ": " + sequencer[currentBeat][i].object.name)
					tiles[currentBeat+BEATS*i].SendColor(WHITE)
					MidiOn(sequencer[currentBeat][i].object.midi)

				else:
					print(str(currentBeat) + ": niks")
					tiles[currentBeat+BEATS*i].SendColor(WHITE)

	pygame.display.flip()

	clock.tick (60)

pygame.quit()
