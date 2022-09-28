#
#	File Conversions
#
def convertFile(srcFile,objFile,name,fudge):
	bin = open(srcFile,"rb").read()
	code = []
	for b in bin:
		code.append(str(ord(b)))

	if fudge == 1:					# fudge VIP monitor to accept RAM in non-1k units
		code[0x1C] = "1"
	if fudge == 2:					# fudge S2 ROM to not wait for B1.
		code[0x3E] = "56"
	out = ",".join(code)
	f = open(objFile,"w")
	f.write("/* GENERATED */\n\nstatic PROGMEM prog_uchar "+name+"["+str(len(code))+"] = {"+out+"};")	
	f.close()

convertFile("monitor.rom","monitor_rom.h","_monitor",1)
convertFile("studio2.rom","studio2_rom.h","_studio2",2);