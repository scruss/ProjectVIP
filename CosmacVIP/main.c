//*******************************************************************************************************
//*******************************************************************************************************
//
//      Name:       Main.C
//      Purpose:    Main program.
//      Author:     Paul Robson
//      Date:       28th February 2013
//
//*******************************************************************************************************
//*******************************************************************************************************

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "general.h"
#include "cpu.h"
#include "hardware.h"
#include "debug.h"

//*******************************************************************************************************
//                                              Main Program
//*******************************************************************************************************

int main(int argc,char *argv[])
{
    BOOL quit = FALSE;
    IF_Initialise();                                                                    // Initialise the hardware
    DBG_Reset();
    int i;
    for (i = 1;i < argc;i++) DBG_LoadFileToAddress(argv[i]);

    #ifdef LOAD_TEST_STUFF
    #ifndef ARDUINO_VERSION
    #ifdef IS_COSMACVIP
    DBG_LoadFileToAddress("../Miscellany/chip8.rom@0");
    DBG_LoadFileToAddress("../Miscellany/brix.ch8@200");
    #endif
    #ifdef IS_ELF
    DBG_LoadFileToAddress("../Testing/speed.asm.bin@0");
    #endif
    #endif
    #endif

    while (!quit)                                                                       // Keep running till finished.
    {
        DBG_Execute();
        quit = IF_Render(TRUE);
    }
    IF_Terminate();
    return 0;
}
