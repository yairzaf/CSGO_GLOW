

import win32api
import win32gui
import win32process
import pymem
import sys
import os

'''OFFSETS....'''
local_offset = 0xC618AC
dwGlowObjectManager = 0x517D930
m_iGlowIndex = 0xA344
m_iTeamNum = 0xF0
dwEntityList = 0x4C3E674

'''OPENING CSGO PROCESS'''
hWnd = win32gui.FindWindow(0, ("counter-Strike: Global Offensive"))
if(hWnd):
    pid=win32process.GetWindowThreadProcessId(hWnd)
    handle = pymem.Pymem()
    handle.open_process_from_id(pid[1])
else:
    print("CSGO wasn't found")
    os.system("pause")
    sys.exit()
    
'''GETTING CLIENT DLL MODULE ENTERY ADDRESS'''
list_of_modules=handle.list_modules()
while(list_of_modules!=None):
    tmp=next(list_of_modules)
    if(tmp[0].name=="client_panorama.dll"):
        client_dll=tmp[1]
        break;

'''GETTING ClocalPlayer'''
local_player_ptr = 0
local_player_ptr = handle.read_bytes(client_dll+local_offset,4)
while(local_player_ptr == 0):
    local_player_ptr = handle.read_bytes(client_dll+local_offset,4)
local_player_ptr= int.from_bytes(local_player_ptr,byteorder='little')


F6=win32api.GetKeyState(0x75)
while(win32api.GetKeyState(0x75)==F6):  
    glow_obj = handle.read_bytes(client_dll+dwGlowObjectManager,4)
    glow_obj = int.from_bytes(glow_obj,byteorder='little')
    my_team= handle.read_int(local_player_ptr+m_iTeamNum)
    for i in range(64):
        entity = handle.read_bytes(client_dll+dwEntityList + i * 0x10,4)
        entity = int.from_bytes(entity,byteorder='little')
        if(entity!=0):
            team = handle.read_int(entity+m_iTeamNum)
            gindex=handle.read_int(entity+m_iGlowIndex)
            if(3==team):
                handle.write_float(glow_obj+((gindex*0x38)+0x4),0.0)
                handle.write_float(glow_obj+((gindex*0x38)+0x8),0.0)
                handle.write_float(glow_obj+((gindex*0x38)+0xc),1.5)
                handle.write_float(glow_obj+((gindex*0x38)+0x10),0.9)
            else:
                handle.write_float(glow_obj+((gindex*0x38)+0x4),1.5)
                handle.write_float(glow_obj+((gindex*0x38)+0x8),0.0)
                handle.write_float(glow_obj+((gindex*0x38)+0xc),0.0)
                handle.write_float(glow_obj+((gindex*0x38)+0x10),0.9)
            handle.write_uchar(glow_obj+((gindex*0x38)+0x24),1)
            handle.write_uchar(glow_obj+((gindex*0x38)+0x25),0)
        
