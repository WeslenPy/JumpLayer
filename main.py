from gcodeparser import GcodeParser
import os 

GCODES_IGNORE = [
  "G",
]


class JumpLayer:
  def __init__(self,filename) -> None:
    self.filename = filename
    
    self.file = self.load_file()
    
    self.gcode = GcodeParser(gcode=self.file)
    
    
  def load_file(self)->str:
    if os.path.exists(self.filename):
      with open(self.filename, 'r') as f:
        return f.read()
    else:
      print("G-code not found!")
      raise os._exit(-1)
    
  def get_pos_layer(self,layer:int)->int:
    
    layers:list[float] = []
    
    result = False
    
    def get_z(param:dict)->bool:
      return param.get("Z",False)
    
    
    for x,i in enumerate(self.gcode.lines):
      layer_z  = get_z(i.params)
        
      if isinstance(layer_z,float):
        if layer_z not in layers:layers.append(layer_z)
          
        if len(layers)==layer:
          result = x
          break
        
    return result
    
  def jump_layers(self,position_layer)->str:
    lines = self.gcode.lines
    
    before_lines = lines[:position_layer]
    new_lines = lines[position_layer:]
    
    new_gcode = ""
      
    before_add = []
    for before in before_lines:
      if before.command[0] not in GCODES_IGNORE:
        if before.command[-1] not in before_add:
          before_add.append(before.command[-1])
          new_gcode+=before.gcode_str+"\n"
          

    for new in new_lines:
      new_gcode+=new.gcode_str+"\n"
      
      
      
    return new_gcode
  
  def save_gcode(self,gcode:str,filename="new_gcode.gcode")->None:
    with open(filename,mode="+w") as f:
      f.write(gcode)

  

if __name__ == "__main__":
  
  
  jump = JumpLayer(filename="BOX_OUTLET.gcode")
  position_layer = jump.get_pos_layer(layer=104)
  if position_layer==False:print("Layer not found!")
  else:
    new_gcode = jump.jump_layers(position_layer=position_layer)
    jump.save_gcode(gcode=new_gcode,filename="new_gcode_v1.gcode")
  
  