
# starting off from a base of 1.25:1 H:W panes

pane_small_w = 15
pane_med_w   = 18
pane_lg_w    = 22

# close enough...
pane_small_h = 12
pane_med_h = 14
pane_lg_h = 18

pane_ratio_sq_wide = 1.25
pane_ratio_sq      = 1.0
pane_ratio_tall_regular = 2.0
pane_ratio_very_tall    = 2.75

window_min_width = 20.0

# 2 pane window sizes

window_sm_default_width = 2 * pane_small_w
window_med_default_width = 2 * pane_med_w 
window_lg_default_width = 2 * pane_lg_w 

window_min_height = 36.0

# total allowance of 20" from floor and zero from top 
window_max_height = floor_height - 20.0

window_max_width  = face_width

# this, but minus whatever pane width
window_kwc_picture_w = face_width - ( 2 * pane_width )
window_kwc_full_w = face_width

window_kwc_reg_w = pane_width * 2 
window_kwc_med_w = pane_width * 3 

# ---
# FACE WIDTHS
# derive these from the pane units directly...

# 6 med panes
major_face_width_sm = 108 

# 8 sm panes
major_face_width_med = 120

# evenly divides by pane_med_w - 8 panes across
major_face_width_lg = 144

# exactly 16 med panes (or 14 with space)
major_face_width_double = 288

# MED - faces that can still have a minor window

med_face_width_sm = 60

med_face_width_med = 72

med_face_width_lg = 84

# MIN - faces without a window
# this is the only constraint worth placing
minor_face_width_min = 48

#-- 
# How to carve up the vertical space?
# 36" default from-bottom = 3 x pane_sm_h


floor_height_sm = 108
floor_height_med = 120 
floor_height_lg  = 144

window_from_floor_min = pane_med_h 
window_from_floor_default = 36.0


'''
lg-picture
    n panes wide, n-1 pane window width, 0.5 pane each side
picture
    n panes wide, n-2 pane window width, 1 pane each side
sm-picture
    n panes wide, n - (1/2n) pane window, 1/4n each side
full-width
    n panes wide, n pane window width

two-bedroom-window
    n panes wide, 2-3 pane window width x 2, 1 or 2 panes between, rest around
    10 wide - 2 / 2 / 2 / 2 / 2
    9 wide -  1 / 3 / 1 / 3 / 1
    etc.


default-sill
    3 panes
low-sill
    2 panes
high-sill
    4 panes

default-above
    1 pane
none-above
    0
two-above
   
1. choose pane unit
2. determine major face width - even number of panes
3. determine minor face widths in terms of panes
4. draw footprint
5. partition floor window layouts
6. draw and place wall loops and windows
7. floor separators and fascia etc



