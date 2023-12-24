import pymem
import keyboard
import time
import sys
import ctypes
from utils import Utils
from entity import Entity
import win32gui
import pygame
import win32api
import win32api
import win32con
import win32gui
from ctypes import windll

#dwForceJump = (0x16BC200)
dwLocalPlayerController = (0x1810F58)
m_fFlags = (0x63)
dwLocalPlayerPawn = (0x16C8F48)
dwEntityList = (0x17C1960)
m_hPlayerPawn = (0x7EC)
playerPos = (0x1224)
m_iHealth = 0x32C
m_hpawn = 0x60C 
m_dwBoneMatrix = 0x26A8
m_iszPlayerName = 0x640
m_iTeamNum = 0x3BF

class GH:
    def __init__(self):
        self._pid = None
        self._engine = None
        self._client = None
        self.mem = None
        self.mePawn = None
        self.offsets = {} 
        self.patterns = {}
        self.UT = None
        self.hwnd = None
        self.rect = None

  #  def read_vec3d(self, entity_pawn):
    #  return [self.mem.read_float(entity_pawn + playerPos), self.mem.read_float(entity_pawn + playerPos+0x4), self.mem.read_float(entity_pawn + playerPos+0x8)]

   

    
    def attach(self):
       # mem = pymem()
       try:
         self.mem = pymem.Pymem("cs2.exe")
         self.UT = Utils(self.mem, self.offsets)

         #self._handle.list_modules()
         modules = (self.mem.list_modules())
         for module in modules:
               print(module.name)

         self._client = pymem.process.module_from_name(self.mem.process_handle, "client.dll").lpBaseOfDll
         self.hwnd = self.UT.GetHwndByPid(self.mem.process_id)
         self.rect = win32gui.GetClientRect(self.hwnd)
         print(self.rect)
         return True
       except:
         print("Attaching/Init Failed")
         pymem.process.close_handle(self.mem.process_handle)
         return False
         



    def playerPos(self):
     # while(1):
         entity_list = self.mem.read_ulonglong(self._client + self.offsets["entList"])
   
         player = self.mem.read_ulonglong(self._client + dwLocalPlayerController)
         #pawn = self.mem.read_ulonglong(player+ m_hPlayerPawn)
        # entry = self.mem.read_ulonglong(entity_list + 0x10 + 0x8 * ((pawn & 0x7FFF) >> 9))
       #  playerPawn = self.mem.read_ulonglong(self._client + dwLocalPlayerPawn)
         self.mePawn = playerPawn
         return self.UT.read_vec3d(playerPawn)
      

         print(str(pos[0]) + ',' + str(pos[1]) + ',' + str(pos[2]))




    def scanTesting(self):
       # print(self.patterns)
        self.patterns["entList"] = rb"\x48\x8B\x0D....\x48\x89\x7C\x24.\x8B\xFa\xC1\xEB"
        entTest = self.mem.pattern_scan_module(self.patterns["entList"], "client.dll")
        displacement = self.mem.read_int(entTest+int(3))
      #  print(displacement)
        displacement += 0x7
       # displacement += sys.getsizeof(displacement)
       # print(entTest)
        print(dwEntityList)

        print((entTest - self._client + displacement))
        self.offsets["entList"] = ((entTest - self._client + displacement))
       # print(displacement)
        
    def get_entities(self):
     ent_list = []
     entity_list =  self.mem.read_ulonglong(self._client + self.offsets["entList"])
     for i in range(1, 64):
         
         #if g_dw_ent_list == 0:
               # continue
         print(i)
         list_entry_ptr = self.mem.read_ulonglong(entity_list + (8 * (i & 0x7FFF) >> 9) + 16)
         if list_entry_ptr == 0:
                continue
         controller_ptr = self.mem.read_ulonglong(list_entry_ptr + 120 * (i & 0x1FF))
         if controller_ptr == 0:
                continue
         controller_pawn_ptr = self.mem.read_ulonglong(controller_ptr + m_hPlayerPawn)
         if controller_pawn_ptr == 0:
                continue

         list_entry_ptr = self.mem.read_ulonglong(entity_list + 0x8 * ((controller_pawn_ptr & 0x7FFF) >> 9) + 16)
         if list_entry_ptr == 0:
                continue
         pawn_ptr = self.mem.read_ulonglong(list_entry_ptr + 120 * (controller_pawn_ptr & 0x1FF))
         if pawn_ptr == 0:
                continue

         

         ent_list.append(Entity(controller_ptr, pawn_ptr, self.UT.get_bones(pawn_ptr), self.UT.get_pos(pawn_ptr), self.mem.read_string(controller_ptr + m_iszPlayerName, 256), self.mem.read_int(pawn_ptr + m_iTeamNum) ))
     return ent_list
    
    def print_poses(self, entlist):
       # myPos = self.UT.read_vec3d(self.mem, self.mePawn)
        for ind, i in enumerate(entlist):
            pos = self.UT.get_pos(i.pawnptr)
            print("Entity: " + str(ind+1))
            print(str(pos[0]) + ',' + str(pos[1]) + ',' + str(pos[2]))

    def drawTest(self):
      Width = win32api.GetSystemMetrics(0)
      Height = win32api.GetSystemMetrics(1)

      pygame.init()
      pygame.mixer.init()
      pygame.display.set_caption("Overlay")
      SetWindowPos = windll.user32.SetWindowPos
      screen = pygame.display.set_mode((Width, Height))
      clock = pygame.time.Clock()
      alpha = 128
      FPS = 60

      bg_color = (0, 0, 0)
      hwnd = pygame.display.get_wm_info()["window"]
      win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
         win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
      win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*bg_color), 0, win32con.LWA_COLORKEY)
      win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
         win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

      color = (160, 32, 240)

      while(1):
         clock.tick(FPS)
         screen.fill(bg_color)
         screen.set_alpha(128)
         #pygame.draw.line(screen,color, 30,30)

         view = self.UT.getViewMatrix()

         entities_list = self.get_entities()
        # print(entities_list)
         print(len(entities_list))

         for Entity in entities_list:
            Entity.updateBones(self.UT.get_bones(Entity.pawnptr))
            self.UT.draw_bones(Entity, win32api.RGB(200,200,200),2)

         if(keyboard.is_pressed("esc")):
                   break

    def detatch(self):
      pymem.process.close_handle(self.mem.process_handle)
      print("Exiting")
      return True


            
        
        
        



def main():
   entry = GH()

   entry.attach()
   entry.scanTesting()
  # entry.playerPos()
   entities = entry.get_entities()
   entry.print_poses(entities)
   for i in entities:
      i.getInfo()
   #entry.drawTest()

  # entry.detatch()





if __name__ == "__main__":
    main()