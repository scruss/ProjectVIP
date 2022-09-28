#!/usr/bin/python2
# *****************************************************************************************************************************
# *****************************************************************************************************************************
#
#				Transmit - a program for communicating with the arduino 1802 emulation to upload binary files.
#
#												Written by Paul Robson March 2013
#
#	The only change needed may be to defaultConnector(self) which is about 40 lines down from here. This sets the default port
#	used by pyserial. The normal pyserial default almost certainly won't work. This should be the same as the port you connect
#	to the Arduino with - on my Linux Box it s /dev/ttyUSB0 as you can see. Windows is probably COM3 or something like that.
#
#	pyserial is at http://pyserial.sourceforge.net 
#
#	Operation: Hold down 'F' (probably D), run python script with files as parameters downloaded sequentially from $0000
#	(e.g. python2 transmit.py chip8.rom ufo.ch8) DTR resets arduino then buzzes, release 'F' and should boot :)
#
#	Hence this is relying on the Arduino's DTR reset functioning. If not you will have to press and hold 'F' and then reset it.
#	On my system running the Arduino IDE appears to turn this DTR reset off completely which is odd.
#
#	For Python v2.7
#	
# *****************************************************************************************************************************
# *****************************************************************************************************************************

import serial,sys,time																# This program needs pyserial installed.

#
#	Possibly the simplest logger in the world.....
#

class Logger:
	def log(self,message):
		print message

#
#	This class is responsible for talking to the serial hardware. It could be replaced by a clss
#	with the same interface which simply collects the characters sent to it and stores them, 
#	so they could be uploaded via a Terminal if you can't get this to work.
#

class SerialConnector:
	def __init__(self,target = ""):
		target = target if target != "" else self.defaultConnector()				# Pick up the default if no target 
		self.connector = serial.Serial(target,9600,timeout = 1)						# Open the serial port at 9600 baud.
		time.sleep(3)																# Sleep while the Arduino resets itself.


	def defaultConnector(self):														# The default port. This is for my Linux box
		return "/dev/ttyUSB0"														# this may well be COM1, COM3 for Windows
																					# (see pyserial documentation)

	def transmit(self,character):													# send a single character to the Serial Port.
		if len(character) != 1:														# check it is just one character
			raise Exception("CODE ERROR:Only send one character a time")
		self.connector.write(character)												# write it to the serial port.
		#print ">>"+character

	def close(self):																# close the serial port when finished.
		self.connector.close()

#
#	This class functions like a file-writer for the SerialConnector - you open it, write bytes to it
#	and close it. It takes care of checksumming etc.
#

class SerialFileWriter:
	def __init__(self,debug = None,connector = SerialConnector()):
		self.connector = connector 													# save the connector.
		self.debug = debug 															# save the logger
		self.hex = "0123456789ABCDEF"												# lazy decimal -> ASCII Hex conversion.

	def open(self):																	# open for writing.
		self.checksum = 0															# zero the current checksum.
		self.connector.transmit("@")												# tell the receiver to zero the checksum.

	def write(self,data):
		if data < 0 or data > 255:													# check for legal value.
			raise Exception("CODE ERROR: Data out of 0-255 range written")
		self.checksum = (self.checksum + data) % 256								# update the byte checksum.
		self._writeByte(data)														# write it out 
		self.connector.transmit("+")												# tell the reciver to store it and bump address

	def writeFile(self,fileName):													# write a whole file out.
		f = open(fileName,"rb")														# open the file for reading.
		bytes = f.read(8192)														# read all the bytes in.
		f.close()																	# close file.
		self._log("Read file {0} length {1} bytes".format(fileName,len(bytes)))
		self._log("Beginning transmission")
		for b in bytes:																# write all the bytes out.
			self.write(ord(b))
		self._log("Completed.")

	def close(self):																# close the current write.
		self._writeByte(self.checksum)												# write out the checksum value
		self.connector.transmit("=")												# tell the receiver to do a checksum test
		self._log("Checksum sent.")

	def terminate(self):															# now finished.
		self.connector.transmit("$")												# tell the receiver to run.
		self.connector.close()														# close the connector.
		self._log("Terminating connection and starting emulation.")

	def _writeByte(self,byteData):													# write a byte out.
		self.connector.transmit(self.hex[byteData/16])
		self.connector.transmit(self.hex[byteData%16])

	def _log(self,message):															# message log.
		if self.debug != None:
			self.debug.log(message)		

#
#	Sample code if you want to automate it. The Logger() and SerialConnector() instances are optional.
#
def sampleAutomation():
	sfw = SerialFileWriter(Logger(),SerialConnector())
	sfw.open()
	sfw.writeFile("chip8.rom")
	sfw.writeFile("ufo.ch8")
	sfw.close()
	sfw.terminate()

#sampleAutomation()

writer = SerialFileWriter()
writer.open()
for f in sys.argv[1:]:
	writer.writeFile(f)
writer.close()
writer.terminate()

