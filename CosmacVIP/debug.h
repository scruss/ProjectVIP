//*******************************************************************************************************
//*******************************************************************************************************
//
//      Name:       Debug.H
//      Purpose:    Debugger Header
//      Author:     Paul Robson
//      Date:       28th February 2013
//
//*******************************************************************************************************
//*******************************************************************************************************

#ifndef _DEBUG_H
#define _DEBUG_H

void DBG_Reset();
void DBG_Execute();
void DBG_LoadChip8();
void DBG_LoadFile(char *fileName,int address);
void DBG_LoadData(WORD16 address,BYTE8 *data,WORD16 length);
void DBG_LoadFileToAddress(char *cmd);

#endif // _DEBUG_H
