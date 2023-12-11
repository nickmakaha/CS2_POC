import pymem
import keyboard
import time

dwForceJump = (0x16BC200)
dwLocalPlayerController = 0x180ACA0
m_fFlags = (0x63)
dwLocalPlayerPawn = (0x16C2D98)
dwEntityList = (0x17BB820)
m_hPlayerPawn = (0x7CC)

class GH:
    def __init__(self):
        _pid = None
        _engine = None
        _client = None
        _handle = None
        dwForceJump = 0x16BC200
        dwLocalPlayer = 0x180ACA0
        m_fFlags = 0x63
    
    def attach(self):
       # mem = pymem()
        self._handle = pymem.Pymem("cs2.exe")
        #self._handle.list_modules()
        modules = (self._handle.list_modules())
        for module in modules:
            print(module.name)

        self._client = pymem.process.module_from_name(self._handle.process_handle, "client.dll").lpBaseOfDll

       # pymem.process.close_handle(self._handle.process_handle)

    def runBHOP(self):
        while(1):
            #try:
                if keyboard.is_pressed("space"):
                    print(":)")
                    entity_list = self._handle.read_ulonglong(self._client + dwEntityList)
 
                    localPlayer = self._handle.read_ulonglong(self._client + dwLocalPlayerController)
                    localPawn = self._handle.read_uint(localPlayer + m_hPlayerPawn)
 
                    onGround = self._handle.read_uint(localPlayer + m_fFlags)
                    

                    print(onGround)
                   # print(self._handle.read_uint(localPla))
                if(keyboard.is_pressed("esc")):
                    break
          #  except:
                #pymem.process.close_handle(self._handle.process_handle)
               # print("failed")
               # break
    
        pymem.process.close_handle(self._handle.process_handle)
            
        time.sleep(.002)



def main():
   entry = GH()

   entry.attach()
   entry.runBHOP()





if __name__ == "__main__":
    main()