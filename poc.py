import pymem
import keyboard
import time
import sys
import ctypes
from utils import Utils

#dwForceJump = (0x16BC200)
dwLocalPlayerController = (0x1810F58)
m_fFlags = (0x63)
dwLocalPlayerPawn = (0x16BC5B8)
dwEntityList = (0x17C1960)
m_hPlayerPawn = (0x7EC )
playerPos = (0x1224)
m_iHealth = 0x32C

class GH:
    def __init__(self):
        self._pid = None
        self._engine = None
        self._client = None
        self.mem = None
        self.offsets = {} 
        self.patterns = {}
        self.UT = Utils()

  #  def read_vec3d(self, entity_pawn):
    #  return [self.mem.read_float(entity_pawn + playerPos), self.mem.read_float(entity_pawn + playerPos+0x4), self.mem.read_float(entity_pawn + playerPos+0x8)]

   

    
    def attach(self):
       # mem = pymem()
        self.mem = pymem.Pymem("cs2.exe")
        #self._handle.list_modules()
        modules = (self.mem.list_modules())
        for module in modules:
            print(module.name)

        self._client = pymem.process.module_from_name(self.mem.process_handle, "client.dll").lpBaseOfDll

       # pymem.process.close_handle(self._handle.process_handle)

    #def runBHOP(self):
    #    while(1):
    #        #try:
       #         if keyboard.is_pressed("space"):
        #            print(":)")
        #            entity_list = self._handle.read_ulonglong(self._client + dwEntityList)
 
        #            localPlayer = self._handle.read_ulonglong(self._client + dwLocalPlayerController)
         #           localPawn = self._handle.read_uint(localPlayer + m_hPlayerPawn)
 
          #          onGround = self._handle.read_uint(localPlayer + m_fFlags)
                    

             #       print(onGround)
                   # print(self._handle.read_uint(localPla))
             #   if(keyboard.is_pressed("esc")):
               #     break
          #  except:
                #pymem.process.close_handle(self._handle.process_handle)
               # print("failed")
               # break
    
       # pymem.process.close_handle(self._handle.process_handle)
            
       # time.sleep(.002)

    def playerPos(self):
      while(1):
         entity_list = self.mem.read_ulonglong(self._client + self.patterns["entList"])
   
         player = self.mem.read_ulonglong(self._client + dwLocalPlayerController)
         pawn = self.mem.read_ulonglong(player+ m_hPlayerPawn)
         entry = self.mem.read_ulonglong(entity_list + 0x10 + 0x8 * ((pawn & 0x7FFF) >> 9))
         playerPawn = self.mem.read_ulonglong(entry + 0x78 * (pawn & 0x1FF))
         pos = self.UT.read_vec3d(self.mem, playerPawn)
      

         print(str(pos[0]) + ',' + str(pos[1]) + ',' + str(pos[2]))
        # print(self.mem.read_int(player + m_iHealth))
         if(keyboard.is_pressed("esc")):
                   break



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
        self.patterns["entList"] = ((entTest - self._client + displacement))
       # print(displacement)
        

        
        
        



def main():
   entry = GH()

   entry.attach()
   entry.scanTesting()
   entry.playerPos()





if __name__ == "__main__":
    main()