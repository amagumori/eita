# a relational language for procedural generation

## defining a schema, then relationship constraints between dimension values.

---

### layout

  footprint - major, med, minor labeling

  style rules - full-width window, full-width awning/balcony etc decisions
    inset windows?
    inset balconies?

      later on - face profiles (more complex than rect), balcony profiles etc.

  window layout style rules -
    full-width (wide, full)

    big-proportion-of-face window - 2 or 3 per face (this is a relation to window-size / face-size)

    small-proportion-of-face window - revert to "small window" sizing - 24-36in w etc.

    tiny-window - small, sparse on med and minor faces
  
### grammar file:

style
  global style rules here - wraparound windows?  awnings chance?  window cages?etc.

footprint 
  width (WIDTH)
  depth (DEPTH)
  
  FACE (left):

    major / med / min ?

    corner chamfer ? corner cutout ?
      chamf relative size ( hi / med / low ) ( >window or <window)
        or
      cutout width / depth
        
    subfaces ?
      subface relative size (hi / med / low)
      subface relative spacing (hi / med / low)
        derive -> subfaces N
        derive -> subface width N
        derive -> subface spacing N
      subface relative depth (hi / med / low)
        derive -> subface depth N

  
etc etc.  you get a list of footprint verts.
make dict of vert pairs -> face data    
    
wall-edges (wall-loops) routine
  this gives you width of "window box"

dimension "window box" vertically:

  window height
  height of "above window"
  height of "under window" (distance from floor to window) 
    these 3 are interrelated and fall in a small range
    window height from ground / balcony height are usually a standard dimension
    or window is floor to ceiling or almost so.

    MAIN CASES AND CONSTRAINTS:
      under-window and window-height are equal or close - no "above-window"
      under-window and above-window are equal - window height varies in small range.
      ratio of 3:below 2:window 1:above
      under-window is small and window-height is the rest.  ratio of 1:under to 2-3:window

dimension "window box" horizontally:

  what kind of face is it?
    
  major:
    full-width
    small number of wider windows per face
    bigger number of "small-standard (24") windows per face
  med:
    small number of wider
    small number of smaller
  min:
    very sparse (1 or 2) tiny windows
    
dimension window:

  split-top? grid? single? split-vertically?

  inset?

  pane size falls in very standardized range
  
dimension under-window:
  
  balcony?  inset / outset

dimension above-window ... is there anything?  awning etc.

place pipes, facade stuff / pillars, clothes hangers, ACs...
    


### window

{PRIORITY} NAME RANGE (DEPENDENCIES) ...constraints later

