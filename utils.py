
playerPos = (0x1224)
    
class Utils:
  def __init__(self):
    pass
  def read_vec3d(self, mem, entity_pawn):
    return [mem.read_float(entity_pawn + playerPos), mem.read_float(entity_pawn + playerPos+0x4), mem.read_float(entity_pawn + playerPos+0x8)]
