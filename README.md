### eita 
Blender addon for procedurally generating buildings

## Relationships and dependencies


### layout settings 

distance between windows
  > window width
  < building width / depth

window-pillar distance 
  distance from ctr of window to pillar origin

  > 0.5 * window width
  < distance between windows

  ideally geometric relationship between this, distance between windows, and etc


### window settings

window width 
  < distance between windows
  < 2 * window-pillar distance

window height
  < floor height
  + offset < floor height (offset pushes up )

window offset
  
  0 = bottom verts of window quad at floor height

  default should be (0.5 * floor height) - ( 0.5 * window height )

  MAX: floor height - window height
  MIN: 0




### Balconies (internal)

this involves actually pushing the window part in, "balcony" flush with facade.

### Balconies (external)

This will be an extension of "floor separator" using layout.wall loops

we need a balcony section to be extruded

balcony depth
balcony "thickness" + chamfer if 


* chamfer horiz?
chamfer underneath?

solid or railing

PER-WINDOW
PER-N-WINDOW ( DIVISIBLE BY N_WINDOWS OBVIOUSLY)

FULL-FLOOR NO WRAP
FULL-FLOOR, WRAP N SIDES
FULL-FLOOR, WRAPAROUND




### About
Fork of @Isimic's project [ProceduralBuildingGenerator](https://github.com/lsimic/ProceduralBuildingGenerator)

![latest commit: grid-type windows](screenshot.png)

### License

GPL-3.0
