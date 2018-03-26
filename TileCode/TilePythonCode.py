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
TURQ	=	"000255000"

#MQTT Constants
BROKERIP = "192.168.178.40"

#Sequencer Constants
BPM		= 	245		#Beats per Minute
GRID	=	(4,4)	#The layout of the tiles
BEATS	=	8		#The amount of beats to loop 		

TOTALTILES 	= 	GRID[0]*GRID[1]
TPB			=	int(TOTALTILES/BEATS)		#Tiles per beat
MPB         =	1000/(BPM/60)				#Milis per beat

MIDILIST	=	[0,61,62,63,64,65,66,67,68,69,70]

def MidiOn(m):
	midiout.send_message([0x90, m, 120])

def MidiOff(m):
	midiout.send_message([0x80, m, 0])

#PYGAME CONSTANTS
TITLE 	= 	"KLONK"
WIDTH 	= 	200
HEIGHT 	= 	200	

#GameModes
mole = False

#Midi Init
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    midiout.open_port(1)

#TILE CLASS
class Tile():
	def __init__(self, number, beat, row):
		self.id = number
		self.beat = beat
		self.row = row
		self.color = BLACK
		self.mole = False

	def SendColor(self, rgb):
		client.publish("led" + str(self.id),str(rgb) + "1")

	def LightUp(self, rgb, time):
		pass

	def SetMole(self):
		self.mole = True
		self.SetColor(WHITE)

	def SetColor(self, rgb):
		self.color = rgb

#MQTT-------

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
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
				if tempmsg == "1":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 1")
					sequencer[i.beat][i.row] = 1
					i.SetColor("000000255")
				if tempmsg == "2":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 2")
					sequencer[i.beat][i.row] = 2
					i.SetColor("000000255")
				if tempmsg == "3":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 3")
					sequencer[i.beat][i.row] = 3
					i.SetColor("000000255")
				if tempmsg == "4":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 4")
					sequencer[i.beat][i.row] = 4
					i.SetColor("000000255")
				if tempmsg == "5":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 5")
					sequencer[i.beat][i.row] = 5
					i.SetColor("000000255")
				if tempmsg == "6":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 6")
					sequencer[i.beat][i.row] = 6
					i.SetColor("000000255")
				if tempmsg == "7":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 7")
					sequencer[i.beat][i.row] = 7
					i.SetColor("000000255")
				if tempmsg == "8":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 8")
					sequencer[i.beat][i.row] = 8
					i.SetColor("000000255")
				if tempmsg == "9":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 9")
					sequencer[i.beat][i.row] = 9
					i.SetColor("000000255")	
				if tempmsg == "0":
					print("Tile #" + str(i.id) +" and beat #" + str(i.beat) + " are set to: 0")
					sequencer[i.beat][i.row] = 0
					i.SetColor("000000000")
			if subTop == "s":
				if mole and i.mole:
					i.SetColor("000000000")
					print("Got the mole at -> Tile #" + str(i.id))
				i.SendColor(PURPLE)

client = mqtt.Client("RASPBERRY")
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

for i in range(GRID[0]):
	tileGrid.append([])
	for j in range(GRID[1]):
		tileGrid[i].append(tiles[j+i*GRID[1]])

for i in range(BEATS):
	sequencer.append([])
	for j in range(TPB):
		sequencer[i].append(0)

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
				pass
			if event.key == pygame.K_SLASH:
				pass

	if (currentTick - lastTick >= MPB):

		for i in MIDILIST:
			MidiOff(i)

		currentBeat+= 1;
		lastTick = currentTick

		for i in tiles:
			if i.beat != currentBeat:
				i.SendColor(i.color)

		if mole:
			newmole = random.randint(0,len(tiles)-1)
			tiles[newmole].SetMole() 
			print("New Mole = " + str(newmole))

		for i in range(TPB):
			if (currentBeat >= BEATS): 
				currentBeat = 0
				print()

			if (sequencer[tiles[currentBeat+BEATS*i].beat][i] != 0):
				print(str(currentBeat) + ": True")
				tiles[currentBeat+BEATS*i].SendColor("000255000")
				MidiOn(MIDILIST[sequencer[tiles[currentBeat+BEATS*i].beat][i]])

			else:
				print(str(currentBeat) + ": False")
				# tiles[currentBeat+BEATS*i-1].SendColor("000000000")
				tiles[currentBeat+BEATS*i].SendColor("255000000")
				
	pygame.display.flip()

	clock.tick (60)

pygame.quit()
