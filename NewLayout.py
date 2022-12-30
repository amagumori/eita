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

def kwc_gen_footprint( general_params: KWCParams, params: KWCBuildingParams ) -> list:

    # in building_params, give a layout type - major faces with inset med faces in between, etc.
    # eventually return a dict with face type for each vert pair

    footprint = list()

    # max 4:1 width depth ratio
    max_depth_ratio = 4

    room_w = params.room_width * general_params.pane_w
    room_h = params.room_height * general_params.pane_h

    width = room_w * params.building_width
    depth = room_w * params.building_depth

    #depth = random.randint( params.building_width, ( params.building_width * max_depth_ratio ) ) 

    footprint.append( (-0.5 * width, -0.5 * depth, 0 ))
    footprint.append( (-0.5 * width, 0.5 * depth, 0 ))
    footprint.append( (0.5 * width, 0.5 * depth, 0 ))
    footprint.append( (0.5 * width, -0.5 * depth, 0 ))

    return footprint

def kwc_layout( general_params: KWCParams, kwc_params: KWCBuildingParams, footprint: list, door_position: tuple) -> dict:

    building_width = general_params.building_width * general_params.room_w
    building_depth = general_params.building_depth * general_params.room_w

    floor_count = 8
    floor_height = 3
    wall_loops = list()
    for i in range(0, floor_count):
        floor_print = footprint.copy()
        for j in range(0, len(floor_print) ):
            floor_print[j] = ( (footprint[j][0], footprint[j][1], floor_height * i ) )
        wall_loops.append(floor_print)

    for i in range(0, len(footprint) - 1 ):

        vert_start = footprint[i]
        if i == len(footprint) - 1:
            vert_end = footprint[0]
        else:
            vert_end = footprint[i+1]

        length_x = vert_end[0] - vert_start[0]
        length_y = vert_end[1] - vert_start[1]
        length = math.sqrt(length_x * length_x + length_y * length_y)

        # try this
        ww_dist_x = ( room_w / length ) * length_x
        ww_dist_y = ( room_w / length ) * length_y

        if math.isclose( length, building_width ):
            room_count = general_params.building_width

            for j in range(0, room_count):
                offset = ( j * room_w ) - (0.5 * room_w)
                window_pos = ( ( vert_start[0] + ((length_x - ( room_count-1) * ww_dist_x ) / 2 ) + j*ww_dist_x),
                              ( vert_start[1] + ((length_y - ( room_count-1) * ww_dist_y ) / 2 ) + j*ww_dist_y),
                              0)
                window_positions.append(window_pos)

        elif math.isclose( length, building_depth ):
            room_count = general_params.building_depth

            for j in range(0, room_count):
                offset = ( j * room_w ) - (0.5 * room_w)
                window_pos = ( ( vert_start[0] + ((length_x - ( room_count-1) * ww_dist_x ) / 2 ) + j*ww_dist_x),
                              ( vert_start[1] + ((length_y - ( room_count-1) * ww_dist_y ) / 2 ) + j*ww_dist_y),
                              0)
                window_positions.append(window_pos)

        else:
            print('poo poo pee pee')


    result = {
        "window_positions": window_positions,
        #"pillar_positions": pillar_positions,
        "wall_loops": wall_loops
    }
    return result


# eliminate paramsgeneral for now, build out later
def kwc_gen_layout( general_params: KWCParams, kwc_params: KWCBuildingParams, footprint: list, door_position: tuple) -> dict:
    """
    Generates the layout of windows, pillars and walls
    Args:
        params_general: Instance of ParamsGeneral class
        footprint: list(tuple(x,y,z)) - list of tuples where each tuple is an xyz coordinate of the footprint
        door_position: tuple(tuple(x,y,z), rot) - tuple, where first element is the xyz coordinate of the door position,
            and second element is the door rotation on Z axis.
    Returns:
        a dictionary with the following keys
            "window_positions" - list(tuple(tuple(x,y,z), rot)) list of tuples, where each item contains the x,y,z
                position of the window and it's rotation on the z axis.
            wall_loops - list(list(tuple(x,y,z)) - list, containing a list of verts, ie loops to be used for extruding
                walls
    """

    room_w = general_params.pane_w * kwc_params.room_width
    room_h = general_params.pane_h * kwc_params.room_height

    print('roomw: ', room_w)
    print('roomh: ', room_h)

    TEST_door_width = 0.5
    TEST_door_height = 1

    TEST_floor_offset = 0.0
    TEST_floor_height = 3.0
    TEST_floor_count = 8

    window_positions = list()
    wall_loops = list()
    wall_verts = list()
    wall_verts_initial = list()
    is_first_loop = True

    for i in range(0, len(footprint)):
        # assign start and end vertex
        vert_start = footprint[i]
        if i == len(footprint) - 1:
            vert_end = footprint[0]
        else:
            vert_end = footprint[i+1]
        # end if

        # push the first vert into the array
        if is_first_loop:
            wall_verts_initial.append((vert_start[0], vert_start[1], TEST_floor_offset))
        else:
            wall_verts.append((vert_start[0], vert_start[1], TEST_floor_offset))
        # end if;

        # calculate length of edge
        length_x = vert_end[0] - vert_start[0]
        length_y = vert_end[1] - vert_start[1]
        length = math.sqrt(length_x * length_x + length_y * length_y)

        print('length x:', length_x)
        print('length y:', length_y)
        print('LENGTH', length)

        # integer divide by "window unit" width (floor)
        window_count = math.floor( length / room_w )
        window_width_x = (room_w / length) * length_x
        window_width_y = (room_w / length) * length_y

        print("window count: ", window_count )
        print("window width x: ", window_width_x)
        print("window width y: ", window_width_y)

        # window-to-window distances are irrelevant in this method?
        ww_dist_x = room_w
        ww_dist_y = room_w 

        # sanity check here
        if window_count < 0:
            window_count = 0

        # calculate distance between windows on x and y axis
        """
        ww_dist_x = (params_general.distance_window_window / length) * length_x
        ww_dist_y = (params_general.distance_window_window / length) * length_y
        window_width_x = (params_general.window_width / length) * length_x
        window_width_y = (params_general.window_width / length) * length_y

        # calculate distance from window to pillar on x and y axis
        wp_dist_x = (params_general.distance_window_pillar / length) * length_x
        wp_dist_y = (params_general.distance_window_pillar / length) * length_y

        # check whether to generate one or two pillars between windows
        if 2 * params_general.distance_window_pillar >= params_general.distance_window_window:
            has_single_pillar = True
        else:
            has_single_pillar = False
        # end if

        """

        # calculate window and pillar rotation (it's always the same)
        vec_edge = Utils.vec_from_verts(vert_end, vert_start)
        vec_0 = mathutils.Vector((0.0, 1.0, 0.0))
        rot = vec_edge.xy.angle_signed(vec_0.xy) - 0.5 * math.pi

        # calculate door range for calculating intersects
        door_size_x = math.cos(door_position[1])*TEST_door_width
        door_size_y = math.sin(door_position[1])*TEST_door_width
        door_start = (door_position[0][0]-0.5*door_size_x,
                      door_position[0][1]-0.5*door_size_y,
                      TEST_floor_offset)
        door_end = (door_position[0][0]+0.5*door_size_x,
                    door_position[0][1]+0.5*door_size_y,
                    TEST_floor_offset)

        
        # @FIXME  !!
        for j in range(0, int(window_count)):
            # calculate window position
            window_pos = ((vert_start[0] + ((length_x - (window_count - 1) * ww_dist_x) / 2) + j * ww_dist_x),
                          (vert_start[1] + ((length_y - (window_count - 1) * ww_dist_y) / 2) + j * ww_dist_y),
                          TEST_floor_offset
                          )

            # check whether the window intersects with the door, push first floor accordingly
            vert_1 = (window_pos[0] - 0.5 * window_width_x, window_pos[1] - 0.5 * window_width_y, 0)
            vert_2 = (window_pos[0] + 0.5 * window_width_x, window_pos[1] - 0.5 * window_width_y, 0)

            window_loop = list()
            window_positions.append( (window_pos, rot) )

            
            if not (Utils.vert_check_intersect(vert_1, door_start, door_end) or
                    Utils.vert_check_intersect(vert_2, door_start, door_end) or
                    Utils.vert_check_intersect(window_pos, door_start, door_end)):
                window_positions.append((window_pos, rot))
            else:
                # windows intersected with the door and was not pushed
                if(Utils.vert_check_intersect(vert_1, door_start, door_end) and
                        (not Utils.vert_check_intersect(vert_2, door_start, door_end))):
                    window_loop = list()
                    window_loop.append(door_end)
                    window_loop.append((vert_2[0], vert_2[1], TEST_floor_offset))
                    wall_loops.append(window_loop)
                elif(Utils.vert_check_intersect(vert_2, door_start, door_end) and
                     (not Utils.vert_check_intersect(vert_1, door_start, door_end))):
                    window_loop = list()
                    window_loop.append((vert_1[0], vert_1[1], TEST_floor_offset))
                    window_loop.append(door_start)
                    wall_loops.append(window_loop)
                elif(Utils.vert_check_intersect(window_pos, door_start, door_end) and
                     (not Utils.vert_check_intersect(vert_1, door_start, door_end)) and
                     (not Utils.vert_check_intersect(vert_1, door_start, door_end))):
                    window_loop = list()
                    window_loop.append((vert_1[0], vert_1[1], TEST_floor_offset))
                    window_loop.append(door_start)
                    wall_loops.append(window_loop)
                    window_loop = list()
                    window_loop.append(door_end)
                    window_loop.append((vert_2[0], vert_2[1], TEST_floor_offset))
                    wall_loops.append(window_loop)
            # end if
            

            # push all other floors
            for floor in range(1, TEST_floor_count + 1):
                pos = (window_pos[0], window_pos[1], TEST_floor_offset + floor * TEST_floor_height)
                window_positions.append((pos, rot))
            # end for

            # calculate the last vert of this loop, because it is broken by the window
            vert_wall = (window_pos[0] - 0.5 * window_width_x,
                         window_pos[1] - 0.5 * window_width_y,
                         TEST_floor_offset)
            # push it into the loops array
            if is_first_loop:
                wall_verts_initial.append(vert_wall)
                is_first_loop = False
            else:
                wall_verts.append(vert_wall)
                # make a copy of wall verts, implement check and modification for first floor
                loop = list()
                for vert in wall_verts:
                    if not Utils.vert_check_intersect(vert, door_start, door_end):
                        loop.append(vert)
                if len(wall_verts) == len(loop):
                    wall_loops.append(loop)
                elif Utils.vert_check_intersect(wall_verts[len(wall_verts)-1], door_start, door_end) and len(loop):
                    loop.append(door_start)
                    wall_loops.append(loop)
                elif Utils.vert_check_intersect(wall_verts[0], door_start, door_end) and len(loop):
                    loop.insert(0, door_end)
                    wall_loops.append(loop)

                # make a copy of wall_verts for each floor, push for each floor except ground
                for floor in range(1, TEST_floor_count + 1):
                    loop = list()
                    for vert in wall_verts:
                        loop.append((vert[0], vert[1], TEST_floor_offset + floor*TEST_floor_height))
                    wall_loops.append(loop)
                wall_verts.clear()
            # end if

            # calculate the first vert of the next loop and push it into the loops array
            vert_wall = (window_pos[0] + 0.5 * window_width_x,
                         window_pos[1] + 0.5 * window_width_y,
                         TEST_floor_offset)
            wall_verts.append(vert_wall)
        # end while

        # check if this is the last edge, append the layout_verts_initial to the current layout_verts
        if i == len(footprint) - 1:
            verts = wall_verts + wall_verts_initial

            # make a copy of wall verts, implement check and modification for first floor
            loop = list()
            for vert in verts:
                if not Utils.vert_check_intersect(vert, door_start, door_end):
                    loop.append(vert)
            if len(verts) == len(loop):
                wall_loops.append(loop)
            elif Utils.vert_check_intersect(verts[len(wall_verts) - 1], door_start, door_end) and len(loop):
                loop.append(door_start)
                wall_loops.append(loop)
            elif Utils.vert_check_intersect(verts[0], door_start, door_end) and len(loop):
                loop.insert(0, door_end)
                wall_loops.append(loop)

            '''
            # make a copy of wall_verts for each floor, push for each floor except ground
            for floor in range(1, TEST_floor_count + 1):
                loop = list()
                for vert in verts:
                    loop.append((vert[0], vert[1], TEST_floor_offset + floor * TEST_floor_height))
                wall_loops.append(loop)
            wall_verts.clear()
            '''
        # end if
    # end for

    # put all results in a dictionary and return it
    result = {
        "window_positions": window_positions,
        "wall_loops": wall_loops
    }
    return result
#

"""
# we will maybe want in the future gen nonstandard footprint
# can build more complicated arbitrary-poly footprints, etc.

# @TODO also need to implement gen_internal_walls and gen_internal_floors.
# this can be done by using f - build face from footprint.

#def build_footprint( params_footprint: ParamsFootprint ) -> list:

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


