# This script jumps between layers in gcode

## how to use define your layer, the name of your gcode and the output name to save it

```python
jump = JumpLayer(filename="BOX_OUTLET.gcode") # replace for your gcode
position_layer = jump.get_pos_layer(layer=104) # replace for your layer jump
jump.save_gcode(gcode=new_gcode,filename="new_gcode_v1.gcode")  # replace with the name you want to save the gcode output
```
