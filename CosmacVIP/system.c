//*******************************************************************************************************
//*******************************************************************************************************
//
//      Name:       System.C
//      Purpose:    System HW Interface
//      Author:     Paul Robson
//      Date:       14th March 2013
//
//*******************************************************************************************************
//*******************************************************************************************************

#include "general.h"
#include "hardware.h"
#include "system.h"

//*******************************************************************************************************
//                                      Hardware interface
//*******************************************************************************************************

#ifdef IS_COSMACVIP
static char *keys = "X123QWEASDZC4RFV";                                             // Map ASCII keys -> VIP keys
#else
static char *keys = "0123456789ABCDEF";                                             // ELF just use 0-9 A-F as the keypad varies.
#endif

static int nextTime = 0;                                                            // Time of next frame end

BYTE8 SYSTEM_Command(BYTE8 cmd,BYTE8 param)
{
    BYTE8 retVal = 0;
    switch(cmd)
    {
        case HWC_READKEYBOARD:                                                      // Command 0 : read keyboard status - 0-15 or 0xFF
            retVal = IF_KeyPressed(keys[param & 0x0F]);
            break;
        case HWC_UPDATEQ:                                                           // Command 1 : update Q
            IF_SetSound(param != 0);
            break;
        case HWC_FRAMESYNC:
            while (nextTime > IF_GetTime()) {}                                      // Command 2 : Synchronise to 60Hz.
            nextTime = IF_GetTime()+1000/60;
            break;
        case HWC_READIKEY:                                                          // Command 4 : Read I Key Status.
            retVal = IF_KeyPressed('I');
            break;
        case HWC_UPDATELED:                                                         // Command 5 : Update 2 Digit LED Display (ELF)
            break;
        case HWC_SETKEYPAD:                                                         // Command 6 : Set Keypad to player 1 or player 2
            keys = "X123QWEASD______";                                              // Key settings for Studio 2 Player 1, Player 2
            if (param == 2) keys == "M678YUIHJ______";
            break;
    }
    return retVal;
}

