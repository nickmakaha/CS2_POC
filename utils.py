import win32gui
import win32con
import win32process
import pymem
from gdi import *
playerPos = (0x1224)
dwViewAngles = 0x1880DD0
dwViewMatrix = 0x1820160
m_pGameSceneNode = 0x310
m_modelState = 0x160
m_vecOrigin = 0x80
m_iTeamNum = 0x3BF
    
class Utils:
  def __init__(self, mem, offsets):
    self.mem = mem
    self.offsets = offsets
    self._client = pymem.process.module_from_name(self.mem.process_handle, "client.dll").lpBaseOfDll
    self.mex = []
    #self.hack = _hack
    self.draw = None
    self.__draw_bons_a_list = []
    self.__draw_bons_b_list = []
    self.rect = []
    self.hwnd = self.GetHwndByPid(self.mem.process_id)
  def get_pos(self, entity_pawn):
    return [self.mem.read_float(entity_pawn + playerPos), self.mem.read_float(entity_pawn + playerPos+0x4), self.mem.read_float(entity_pawn + playerPos+0x8)]

  def GetHwndByPid(self, _pid):
    hwnd = win32gui.GetTopWindow(0)
    while hwnd:
        t_id, pid = win32process.GetWindowThreadProcessId(hwnd)
        if t_id and pid == _pid and not win32gui.GetParent(hwnd):
            return hwnd
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return 0


  def getViewMatrix(self):
    pass
   # vm = self.mem.read_ulonglong(self._client + dwViewMatrix)
   # self.mex = []

    #for i in range(4):
     # x = self.mem.read_float(vm)
     # y = self.mem.read_float(vm+4)
     # z = self.mem.read_float(vm+4*2)
     # a = self.mem.read_float(vm+4*3)
     # vm += 16
      #self.mex.append((x,y,z,a))

  def get_bones(self, entitypawn):
        bones = []
        scene = self.mem.read_ulonglong(
            entitypawn+m_pGameSceneNode)
        bonearray = self.mem.read_ulonglong(
            scene+m_modelState+m_vecOrigin)
        for i in range(30):
            x = self.mem.read_float(bonearray)
            y = self.mem.read_float(bonearray+4)
            z = self.mem.read_float(bonearray+4*2)
            bones.append((x, y, z))
            bonearray += 0x20
        return bones
  def __update_mex(self):
        self.mex = []
        addr = self._client+dwViewMatrix
        for i in range(4):
            x = self.mem.read_float(addr)
            y = self.mem.read_float(addr+4)
            z = self.mem.read_float(addr+4*2)
            a = self.mem.read_float(addr+4*3)
            addr += 4*4
            self.mex.append((x, y, z, a))

  def world_to_screen(self, pos, update_mex: bool = True) -> list:
        self.rect = win32gui.GetClientRect(self.hwnd)
        if update_mex:
            self.__update_mex()
        view = 0.0
        sightx, sighty = self.rect[2]/2, self.rect[3]/2
        view = self.mex[3][0]*pos[0]+self.mex[3][1] * \
            pos[1]+self.mex[3][2]*pos[2]+self.mex[3][3]

        if view <= 0.01:
            return ()
        x = sightx + (self.mex[0][0] * pos[0] + self.mex[0][1] *
                      pos[1] + self.mex[0][2] * pos[2] + self.mex[0][3]) / view * sightx

        y = sighty - (self.mex[1][0] * pos[0] + self.mex[1][1] *
                      pos[1] + self.mex[1][2] * pos[2] + self.mex[1][3]) / view * sighty
        return x, y


  def get_teamID(self, entity):
    return self.mem.read_int(entity + m_iTeamNum)

  def __push_draw_ab(self, a, b, update_mex: bool = False):
        screen_a = self.world_to_screen(a, update_mex)
        screen_b = self.world_to_screen(b, update_mex)
        if len(screen_a) != 0 and len(screen_b) != 0:
            if (screen_a[0] != 0.0 and screen_a[1] != 0.0) and (screen_b[0] != 0.0 and screen_b[1] != 0.0):
                self.__draw_bons_a_list.append(screen_a)
                self.__draw_bons_b_list.append(screen_b)

  def draw_bones(self, ent_pawn, color, thickness):
      #  self.hwnd = self.GetHwndByPid(self.mem.process_id)
        self.draw = GDI(self.hwnd, hide=False)
        self.__draw_bons_a_list.clear()
        self.__draw_bons_b_list.clear()

        self.__push_draw_ab(ent_pawn.bones[6], ent_pawn.bones[5], True)
        self.__push_draw_ab(ent_pawn.bones[4], ent_pawn.bones[5])
        self.__push_draw_ab(ent_pawn.bones[4], ent_pawn.bones[2])
        self.__push_draw_ab(ent_pawn.bones[2], ent_pawn.bones[0])

        self.__push_draw_ab(ent_pawn.bones[13], ent_pawn.bones[5])
        self.__push_draw_ab(ent_pawn.bones[8], ent_pawn.bones[5])
        self.__push_draw_ab(ent_pawn.bones[13], ent_pawn.bones[14])
        self.__push_draw_ab(ent_pawn.bones[8], ent_pawn.bones[9])
        self.__push_draw_ab(ent_pawn.bones[9], ent_pawn.bones[10])
        self.__push_draw_ab(ent_pawn.bones[10], ent_pawn.bones[11])
        self.__push_draw_ab(ent_pawn.bones[14], ent_pawn.bones[15])
        self.__push_draw_ab(ent_pawn.bones[16], ent_pawn.bones[15])

        self.__push_draw_ab(ent_pawn.bones[0], ent_pawn.bones[25])
        self.__push_draw_ab(ent_pawn.bones[26], ent_pawn.bones[25])
        self.__push_draw_ab(ent_pawn.bones[26], ent_pawn.bones[27])
        self.__push_draw_ab(ent_pawn.bones[0], ent_pawn.bones[22])
        self.__push_draw_ab(ent_pawn.bones[23], ent_pawn.bones[22])
        self.__push_draw_ab(ent_pawn.bones[23], ent_pawn.bones[24])

        self.draw.DrawLine(self.__draw_bons_a_list,
                           self.__draw_bons_b_list, color, thickness)