### eita 
Blender addon for procedurally generating buildings

## EITA - project goals

Eita is aimed to be a "layer cake" of mesh procedural generation routines, aimed to create a vivid, complex, and beautiful megacity environment.

To accomplish this, the goal of the current phase of the project ( generating buildings ) can be seen as generating, understanding, and implementing a taxonomy of building styles.

The original project this is forked from implemented a single style of building representative of european architecture, with pillars, between-floor moldings, window frames, etc.

My current goal is to build a generative setup that can build a variety of tokyo and taiwan-style buildings.  these building styles incorporate more vernacular structures such as corrugated awnings, window-cages, and are more pragmatic in their architectural approach, with less filigree.

### Generation path

The "path" of generating buildings should be broadly:

We have a lot, somehow - we determine earlier whether to generate whole-parcel lot, several smaller building lots, etc

Based firstly off size, determine building style

Determine a specific building TYPE from the style and lot dims, things such as:

  + large apt building, or single unit per floor?
  + single window per floor?
  + inset ground floor + entrance?
  + balconies?  if so:
    + per-window, separate
    + front face only
    + wraparound front and sides
    + wraparound entire 
    
This leads to the idea of a minimum room size / building size for single occupancy / single occupancy per floor

minimum building WIDTH is around 20ft, and in these cases, the depth is much longer, usually 1:3 ratio

this is commensurate with the median size for a "single non-tiny" (1br+) living space.

minimum building DEPTH is at least 30-35ft.

---

from here, we can determine parameters like window count, spacing, etc *a priori* from placing constraints on the minimum size of a room.

1LDK - 8x16 (128ft2)

---

## Zoning

by creating a "zoning" heatmap, we can determine what types of buildings to place when generating lots within parcels.  a more "big-residential" area will generate larger apartment complexes, while a "quiet-residential" area will generate more small, single-occupancy-per-floor type buildings.

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
