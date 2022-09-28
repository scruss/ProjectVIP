#
#	Binary Convertor
#

def convert(sourceFile,name,address,dataFile,execFile):
	f = open(sourceFile,"rb")
	code = []
	bytes = f.read(8192)
	f.close()

	for b in bytes:
		code.append(str(ord(b)))
	size = len(code)
	code = "{" + (",".join(code))+"}"

	execCode = "prog_uchar "+name+"[] PROGMEM = "+code+";"+"\n"
	dataFile.write(execCode)

	execCode = "RAMUpload("+name+","+str(size)+","+str(address)+");\n"
	execFile.write(execCode)

fData = open("binary_data.h","w")
fExec = open("binary_code.h","w")

convert("chip8.rom","chip8",0,fData,fExec)
convert("brix.ch8","brix",512,fData,fExec)

fData.close()
fExec.close()

