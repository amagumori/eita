import bpy
import math
import random
import mathutils
from enum import Enum
from . import Utils

#  12 Alley 21, Lane 69, Section 5, Minsheng E Rd

class FaceType(Enum):
    maj = 1,
    med = 2,
    min = 3

def get_divisors(n):
    for i in range(1, int(n / 2) + 1):
        if n % i == 0:
            yield i
    yield n

def decide ( probability ) -> bool:
    return random.random() < probability

class KWCParams:

    def __init__(self, width, depth, pane_w, pane_h):

        self.width = width 
        self.depth = depth
        self.pane_w = pane_w 
        self.pane_h = pane_h 

        
    def generate_building_params( self ):

        building_width = self.width
        building_depth = self.depth

        major_face_min_window_width = 3
        med_face_min_window_width = 2
        min_face_min_window_width = 1

        pane_w = self.pane_w 
        pane_h = self.pane_h

        # width of a "room" or "face" (not a whole wall)
        room_w = random.randrange( 8, 14 )
        room_h = random.randrange( 8, 10 )   # this doesn't even need to be random

        # divide vertically - hard constraints like under-window and above-window don't vary much
        under_window = random.randrange(2, 3)
        remaining_space = room_h - under_window
     
        rem = remaining_space % pane_h
        if rem == 0:
            space_above_window = decide(0.7)
            if space_above_window == True:
                window_above = 1
                window_height = remaining_space - window_above
            else:
                window_above = 0
                window_height = remaining_space

        else:
            window_above = rem
    

            """
            space_above_window = decide(0.6)
            if space_above_window == True:
                window_above = 1 - rem
            else:
                window_above = 0
            """
        window_around = random.randrange(0, 1)
        window_height = math.floor( room_h - window_above - under_window )
        # full width by default
        window_width = math.floor( room_w - (window_around*2) )

        # don't even do the multiple windows bs 
        # we're going face by face, 1 - 3 windows per and even 3 is a lot

        full_width_window = decide(0.85)
        if ( full_width_window == True ):
            multiple_windows = False

        if ( full_width_window == False ):
            if ( room_w > 16 ):
                multiple_windows = decide( 0.58 )
            else:
                multiple_windows = False

        if ( multiple_windows ):
            
            #around_space = random.randrange(1, 2)
            #between_space = random.randrange(1, 2)
            
            window_around = 1
            windows_between = 2

            available_space = room_w - window_around - windows_between
            divisors = get_divisors( available_space )
            div = np.array(divisors)
            possible_divisors = np.where( div > major_face_min_window_width )
            
            window_width = np.random.choice( possible_divisors )

        # just rock with this for now    
        med_room_w = random.randrange(4, 6)
        med_room_h = room_h
        med_window_height = random.randrange( (window_height-1), window_height )

        # just doing this for now.
        med_window_width = 2
        med_under_window = under_window
        med_above_window = med_room_h - med_under_window - med_window_height

        min_room_w = random.randrange(3, 4)
        match min_room_w:
            case 3:
                min_window_width = 1
            case 4:
                min_window_width = 2

        min_room_h = med_room_h
        min_window_height = med_window_height
        min_under_window = med_under_window
        min_above_window = min_room_h - min_under_window - min_window_height 

        params = KWCBuildingParams(
                building_width,
                building_depth,
                room_w,
                room_h,
                window_width,
                window_height,
                under_window,
                window_above,
                window_around )

        return params

    

    @staticmethod
    def from_ui():
        props = bpy.context.scene.KWCPropertyGroup
        params = KWCParams( props.width, props.depth, props.pane_w, props.pane_h)
        return params

#end KWCParams

class FaceParams:
    def __init__(self, 
                 face_type,
                 room_width,
                 room_height,
                 window_width,
                 window_height,
                 under_window,
                 above_window,
                 around_window):

        self.face_type = face_type
        self.room_width = room_width
        self.room_height = room_height
        self.window_width = window_height
        self.under_window = under_window
        self.above_window = above_window
        self.around_window = around_window

#end FaceParams

class KWCBuildingParams:
    # TODO: docstring
    # this is getting ridiculous.
    def __init__(self,
                 building_width,
                 building_depth,
                 room_width,
                 room_height,
                 window_width,
                 window_height,
                 under_window,
                 above_window,
                 around_window):
                
        self.building_width = building_width
        self.building_depth = building_depth

        self.room_width = room_width
        self.room_height = room_height
        self.window_width = window_width
        self.window_height = window_height
        self.under_window = under_window
        self.above_window = above_window
        self.around_window = around_window

# end KWCBuildingParams

class ParamsGeneral:
    # TODO: docstring
    def __init__(self, floor_count: int, floor_height: float, floor_offset: float, generate_separator: bool,
                 separator_height: float, separator_width: float, window_width: float, window_height: float,
                 window_offset: float, distance_window_window: float, generate_pillar: bool,
                 distance_window_pillar: float, door_width: float, door_height: float):
        self.floor_count = floor_count
        self.floor_height = floor_height
        self.floor_offset = floor_offset
        self.generate_separator = generate_separator
        self.separator_height = separator_height
        self.separator_width = separator_width
        self.window_width = window_width
        self.window_height = window_height
        self.window_offset = window_offset
        self.distance_window_window = distance_window_window
        self.generate_pillar = generate_pillar
        self.distance_window_pillar = distance_window_pillar
        self.door_width = door_width
        self.door_height = door_height
    # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsGeneral(
            floor_count=properties.floor_count,
            floor_height=properties.floor_height,
            floor_offset=properties.floor_first_offset,
            generate_separator=properties.floor_separator_include,
            separator_height=properties.floor_separator_height,
            separator_width=properties.floor_separator_width,
            window_width=properties.window_width,
            window_height=properties.window_height,
            window_offset=properties.window_offset,
            distance_window_window=properties.distance_window_window,
            generate_pillar=properties.generate_pillar,
            distance_window_pillar=properties.distance_window_pillar,
            door_width=properties.door_width,
            door_height=properties.door_height
        )
        return params
    # end from_ui
# end ParamsGeneral

class ParamsFootprint:
    # TODO: docstring
    # this is getting ridiculous.
    def __init__(self, left, bottom, right, top, building_width, building_depth):

        self.building_width = building_width
        self.building_depth = building_depth
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.FootprintPropertyGroup
        params = ParamsFootprint(
            building_width=properties.building_width,
            building_depth=properties.building_depth,
            left=properties.left,
            top=properties.top,
            right=properties.right,
            bottom=properties.bottom
        )
        return params
    # end from_ui
# end ParamsFootprint

class ParamsFootprintFace:
    # TODO: docstring
    def __init__(self, face_type, inset_first_floor):
        
        # chamfers and broad bldg params need to be passed in 
        # to not fuck everything

        # eventually we will stack footprints for different
        # building profiles
        # "bridge_loops" API will be used to bridge bottom footprint loop
        # to top one.

        #self.curved_corner = curved_corner # bool
        #self.corner_chamfer = corner_chamfer
        #self.corner_radius = corner_radius # work on this later.

        self.face_type = face_type # major, med, minor

        # doing the inset stuff per side.
        #self.ff_inset = inset_first_floor  # bool
        #self.ff_from_edge = inset_first_floor_d_from_edge
        #self.ff_inset_depth = inset_first_floor_depth
        #self.ff_inset_chamfer = inset_first_floor_chamfer

        self.subface_count = subface_count
        self.subface_offset = subface_offset
        self.subface_depth = subface_depth # can be negative and outset
        self.subface_width = subface_width

    # end init

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.FacePropertyGroup
        params = ParamsFootprintFace(

            #curved_corner = properties.curved_corner, # bool
            #corner_chamfer = properties.corner_chamfer
            #corner_radius = corner_radius, # work on this later.

            face_type = properties.face_type,
            
            #ff_inset = properties.inset_first_floor,  # bool
            #ff_from_edge = properties.inset_first_floor_d_from_edge,
            #ff_inset_depth = properties.inset_first_floor_depth,
            #ff_inset_chamfer = properties.inset_first_floor_chamfer,

            subface_count = properties.subface_count,
            subface_offset = properties.subface_offset,
            subface_depth = properties.subface_depth, # can be negative
            subface_width = properties.subface_width,

        )
        return params

def kwc_gen_footprint( params: KWCBuildingParams ) -> list:

    footprint = list()

    # max 4:1 width depth ratio
    max_depth_ratio = 4

    width = params.building_width
    depth = params.building_depth

    #depth = random.randint( params.building_width, ( params.building_width * max_depth_ratio ) ) 

    footprint.append( (-0.5 * params.building_width, -0.5 * params.building_depth, 0 ))
    footprint.append( (-0.5 * params.building_width, 0.5 * params.building_depth, 0 ))
    footprint.append( (0.5 * params.building_width, 0.5 * params.building_depth, 0 ))
    footprint.append( (0.5 * params.building_width, -0.5 * params.building_depth, 0 ))

    return footprint


# we will maybe want in the future gen nonstandard footprint
# can build more complicated arbitrary-poly footprints, etc.

# @TODO also need to implement gen_internal_walls and gen_internal_floors.
# this can be done by using f - build face from footprint.

#def build_footprint( params_footprint: ParamsFootprint ) -> list:


"""
minor, med, and major faces

FOOTPRINT SCHEMA
    bottom left, bottom right, top right, top left. CCW
    major face, minor, minor, minor. "rowhouse" type.

    first generalization: rectilinear only.  4 "sides", with insets etc.

width, depth

MAJOR FACE-

    inset/outset face count? (1-4 or so)
    inset-face position/offset: N from left edge
    inset-face depth
    inset-face width
    
    each inset face - minor, med, minor
    med = parallel to major, but set back.

    if inset faces > 1
        distance between inset faces


MED FACE - sides
"""

def new_gen_footprint(params_footprint: ParamsFootprint) -> list:
    """
        Generates the building footprint
    Args:
        params_footprint: Instance of ParamsFootprint class
    Returns:
        list(tuple(x,y,z)) - a list containing ordered verts, which define the building footprint.
    

    this is built with "wedge" face facing north

    if 
    "full-floor non-wrap balconies" then we export lists for each side of the building's flat part"

    want to store:
        MAJOR and MINOR axis of footprint
        a reference to each edge of building
        whether edge is > window-width


    10/29
    (num_faces * face_width) + ( num_faces * face_offset ) < building_width 
    face_depth < 0.3 * building_depth
    """

    width = params_footprint.building_width
    depth = params_footprint.building_depth

    left = params_footprint.left
    bottom = params_footprint.bottom
    right = params_footprint.right
    top = params_footprint.top
  
    """
    major_edge = [
            (-0.5 * params_footprint.building_width, 0.5 * params_footprint.building_depth, 0),
            (0.5 * params_footprint.building_width, 0.5 * params_footprint.building_depth, 0)
    ]
    major_dy = major_edge[1][1] - major_edge[0][1]
    major_dx = major_edge[1][0] - major_edge[0][0]

    # which way is the building pointing.  normal vector of the front face
    # this points out towards the street.
    building_facing = ( major_dy, -major_dx, 0 )
    """


    layout = list()

    # bottom face first

    # bottom left corner
    """
    if left.corner_chamfer > 0:
        layout.append((-0.5 * width + left.corner_chamfer,
                       -0.5 * depth, 0))

        layout.append((-0.5 * width,
                       -0.5 * depth + left.corner_chamfer, 0))
    else:
    """
    layout.append((-0.5 * width, -0.5 * depth, 0))

    marker = -0.5 * depth

    for face in range(left.subface_count):
        # iterating along Y in + direction
        # don't even worry about chamfer for now.
        if marker > 0.5 * depth:
            break

        layout.append((
            -0.5 * width,
            marker + left.subface_offset,
            0 ))

        layout.append((
            (-0.5 * width) + left.subface_depth,
            marker + left.subface_offset,
            0 ))

        layout.append((
            (-0.5 * width) + left.subface_depth,
            marker + left.subface_offset + left.subface_width,
            0 ))

        layout.append((
            -0.5 * width,
            marker + left.subface_offset + left.subface_width,
            0 ))

        marker += left.subface_offset 
        marker += left.subface_width
    
    # top left
    layout.append((
        -0.5 * width,
        0.5 * depth,
        0 ))

    marker = -0.5 * width

    for face in range(top.subface_count):
        # iterating along X in + direction
        # don't even worry about chamfer for now.
        if marker > 0.5 * width:
            break

        layout.append((
            marker + top.subface_offset,
            0.5 * depth,
            0 ))

        layout.append((
            marker + top.subface_offset,
            (0.5 * depth) - top.subface_depth,
            0 ))

        layout.append((
            marker + top.subface_offset + top.subface_width,
            (0.5 * depth) - top.subface_depth,
            0 ))

        layout.append((
            marker + top.subface_offset + top.subface_width,
            (0.5 * depth),
            0 ))

        marker += top.subface_offset 
        marker += top.subface_width

    # top right
    layout.append((
        0.5 * width,
        0.5 * depth,
        0 ))

    marker = 0.5 * depth
    # right
    for face in range(right.subface_count):
        # iterating along Y in - direction
        # don't even worry about chamfer for now.
        if marker <= -0.5 * depth:
            break

        layout.append((
            0.5 * width,
            marker - right.subface_offset,
            0 ))

        layout.append((
            (0.5 * width) - right.subface_depth,
            marker - right.subface_offset,
            0 ))

        layout.append((
            (0.5 * width) - right.subface_depth,
            marker - right.subface_offset - right.subface_width,
            0 ))

        layout.append((
            (0.5 * width),
            marker - right.subface_offset - right.subface_width,
            0 ))

        marker -= right.subface_offset 
        marker -= right.subface_width

    # bottom right
    layout.append((
        0.5 * width,
        -0.5 * depth,
        0 ))
    
    marker = 0.5 * width

    # bottom
    for face in range(bottom.subface_count):
        # iterating along Y in + direction
        # don't even worry about chamfer for now.
        if marker < -0.5 * width:
            break

        layout.append((
            marker - bottom.subface_offset,
            -0.5 * depth,
            0 ))

        layout.append((
            marker - top.subface_offset,
            (-0.5 * depth) + bottom.subface_depth,
            0 ))

        layout.append((
            marker - bottom.subface_offset - bottom.subface_width,
            (-0.5 * depth) + bottom.subface_depth,
            0 ))

        layout.append((
            marker - bottom.subface_offset - bottom.subface_width,
            (-0.5 * depth),
            0 ))

        marker -= bottom.subface_offset 
        marker -= bottom.subface_width

    layout.append( ( -0.5*width, -0.5 * depth, 0 ) )
    
    return layout



def generate_first_floor_print ( footprint: list, params_footprint: ParamsFootprint ) -> list:
    new_footprint = list()
    # just impl this path for now..a
    # inset from edge
    # inset depth
    # chamfer on inset
    building_width = params_footprint.building_width
    inset_from_edge = params_footprint.front_face_inset_from_edge
    inset_depth = params_footprint.front_face_inset_depth
    inset_chamfer = params_footprint.front_face_inset_chamfer


    if params_footprint.building_chamfer > 0:
        # bottom left corner
        new_footprint.append( footprint[0] ) 
        new_footprint.append( footprint[1] )
        
        # top left
        new_footprint.append( footprint[2] )
        new_footprint.append( footprint[3] )

        # inset front face ( pointing +y)
        new_footprint.append((
                footprint[3][0] + inset_from_edge - inset_chamfer,
                footprint[3][1],
                footprint[3][2]))
        new_footprint.append((
                footprint[3][0] + inset_from_edge,
                footprint[3][1] - inset_chamfer,
                footprint[3][2]))

        new_footprint.append((
                footprint[3][0] + inset_from_edge,
                footprint[3][1] - inset_depth + inset_chamfer,
                footprint[3][2]))
        new_footprint.append((
                footprint[3][0] + inset_from_edge + inset_chamfer,
                footprint[3][1] - inset_depth,
                footprint[3][2]))

        new_footprint.append((
                (0.5 * building_width) - inset_from_edge - inset_chamfer,
                footprint[3][1] - inset_depth,
                footprint[3][2]))

        new_footprint.append((
                (0.5 *building_width) - inset_from_edge,
                footprint[3][1] - inset_depth + inset_chamfer,
                footprint[3][2]))

        new_footprint.append((
                (0.5 * building_width) - inset_from_edge,
                footprint[3][1] - inset_chamfer,
                footprint[3][2]))

        new_footprint.append((
                (0.5 * building_width) - inset_from_edge + inset_chamfer,
                footprint[3][1],
                footprint[3][2]))
        
        # we'll end it here and return to the traditional footprint vert placing
        
        # top right (+x +y )
        new_footprint.append((0.5 * params_footprint.building_width - params_footprint.building_chamfer, 0.5 * params_footprint.building_depth, 0))

        new_footprint.append((0.5 * params_footprint.building_width, 0.5 * params_footprint.building_depth - params_footprint.building_chamfer, 0))

        # bottom right
        new_footprint.append((0.5 * params_footprint.building_width, -0.5 * params_footprint.building_depth + params_footprint.building_chamfer, 0))
        new_footprint.append((0.5 * params_footprint.building_width - params_footprint.building_chamfer, -0.5 * params_footprint.building_depth, 0))
        
        return new_footprint 

# later: BlockData as argument

"""
def kwc_gen_params( settings: KWCLayoutParams ) -> KWCLayoutParams:

    ### MAJOR FACE

    # randint for now, in general want to pull from a gausssian distribution
    width  = random.randint( settings.min_width, settings.max_width )
    floor_height = random.randint( settings.min_floor_height, settings.max_floor_height )
    # for simplicity's sake:
    window_below = 1 # 1m

    rem = floor_height - below_window_height

    # remaining height to fill in pane units
    rem_panes_h = rem / settings.pane_h
    min_panes_h = settings.min_window_height / settings.pane_h

    window_height = random.randint( min_panes_h, rem_panes_h )
    window_above = rem - window_height

    # either 0, 1, or 2 panes of wall surrounding the window.
    window_around_space = random.randint(0, 2) 
    window_width = width - (window_around_space*2)

    ### MINOR FACE

    # for now
    # width of one "face unit" ....
    minor_width = width

    minor_window_above = window_above
    minor_window_below = window_below

    minor_window_width = random.randint(1, 3)
    minor_window_height = window_height

    window_around_rem = minor_width - minor_window_width
    minor_window_around = window_around_rem / 2
"""


