import sys
sys.path.insert(0, "/home/pi/python_modules")
import RPi_I2C_driver as i2c
import re
import time
import datetime
import board
#import adafruit_matrixkeypad
from pad4pi import rpi_gpio
from subprocess import Popen, PIPE
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

mylcd = i2c.lcd()

#key_rows = [digitalio.DigitalInOut(x) for x in (board.D21, board.D20, board.D16, board.D12)]
#key_cols = [digitalio.DigitalInOut(x) for x in (board.D26, board.D19, board.D13, board.D6)]
ROW_PINS = [21, 20, 16, 12]
COL_PINS = [26, 19, 13 ,6]

KEYPAD = [[1, 2, 3, "A"],
        [4, 5, 6, "B"],
        [7, 8, 9, "C"],
        ["*", 0, "#", "D"]]
#keypad = adafruit_matrixkeypad.Matrix_Keypad(key_rows, key_cols, keys)
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# wipe LCD screen before we start
mylcd.lcd_clear()

def printKey(key):
	print(key)

# get input from the keypad
def time_input(key):
	time.sleep(0.2)
	mylcd.lcd_clear()
	global lcd_message_input1
	global lcd_message_input2
	global seconds
	if key == 'A':
		lcd_message_input1 = 'ENTER TIME'
		lcd_message_input2 = 'X:XX:XX'
	mylcd.lcd_display_string(lcd_message_input1, 1)
	mylcd.lcd_display_string(lcd_message_input2, 2)
	m = re.compile("X")
#	n = re.compile("^[^X]*")
	o = re.compile("[X0-9:]+$")
#	p = re.compile("[X:]+$")
	q = re.compile("\d+")
	r = re.compile("\d+$")
	print("time_input.key: ", key, " isnumeric: ", key.isnumeric())
	if key.isnumeric() and re.search(".$", lcd_message_input2).group() == 'X':
	# get_keypress
		print("is numeric")
#		for i in range(len(o.search(lcd_message_input2, 0).group())):
		print("time_input -> keypress: ", key)
		lcd_message_input2 = m.sub(key, lcd_message_input2, 1)
		print(lcd_message_input2)
		print(q.search(lcd_message_input2, 0).group())
		mylcd.lcd_display_string(lcd_message_input2, 2)
	if key.isnumeric() and re.search(".$", lcd_message_input2).group() != 'X':
		seconds = int(q.search(lcd_message_input2, 0).group()) * 60 + int(r.search(lcd_message_input2, 0).group())
		print(seconds, " seconds")
	return(0)

def key_press(key):
	return(key)

def previous_time(x):
	mylcd.lcd_display_string(lcd_message_input1, 1)
	mylcd.lcd_display_string(lcd_message_input2, 2)
	time_input(x)
	return(0)

# count down to 0 from the entered value
def countdown_timer(x, now=datetime.datetime.now):
	target = now()
	one_second_later = datetime.timedelta(seconds=1)
	for remaining in range(seconds, -1, -1):
		target += one_second_later
		print(datetime.timedelta(seconds=remaining), 'remaining', end='\r')
		mylcd.lcd_display_string('Time remaining: ', 1)
		mylcd.lcd_display_string(str(datetime.timedelta(seconds=remaining)), 2)
		time.sleep((target - now()).total_seconds())
	mylcd.lcd_clear()
	mylcd.lcd_display_string('A to start', 1)
	mylcd.lcd_display_string('B to repeat', 2)

	return 0
#	print('\nTIMER ended')

def top_switch(key):
	print("top_switch: ", key)
	mylcd.lcd_clear()
	the_switch = {
		'A': time_input,
		0 : time_input,
		1: time_input,
		2: time_input,
		3: time_input,
		4: time_input,
		5: time_input,
		6: time_input,
		7: time_input,
		8: time_input,
		9: time_input,
		'B': previous_time,
		'D': countdown_timer
	}
	# get the function from the_switch
	global mode
	mode = the_switch.get(key)
	func = the_switch.get(key) #, lambda: "Invalid")
	func(str(key))
	return(0)

def a_switch(key, seconds):
	the_switch = {
		'A': time_input,
		'B': previous_time,
		'D': countdown_timer
	}
	func = the_switch.get(key, lambda: "Invalid")
	return(func(key))

#if __name__ == '__main__':
	#while True:


#print("testing pad4pi")
mylcd.lcd_display_string('A to start', 1)
mylcd.lcd_display_string('B to repeat', 2)

#global lcd_message_input1
lcd_message_input1 = 'ENTER TIME'
#global lcd_message_input2
lcd_message_input2 = 'X:XX:XX'
keypad.registerKeyPressHandler(top_switch)

try:
	while True:
		time.sleep(0.2)
except:
	print("cleaning up")
	keypad.cleanup()
#	result = top_switch(key, 0)

