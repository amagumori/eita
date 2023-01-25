import bpy
import math
import random
import mathutils

import pprint 
from collections import namedtuple
from typing import NamedTuple 

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

        #space_between_rooms = 0
        space_between_rooms = random.randrange(0, room_w)

        print("SPACE BETWEEN: ", space_between_rooms )

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
        window_around = random.randrange(0, 2)
        window_height = math.floor( room_h - window_above - under_window )
        # full width by default
        window_width = math.floor( room_w - (window_around*2) )

        # don't even do the multiple windows bs 
        # we're going face by face, 1 - 3 windows per and even 3 is a lot

        full_width_window = decide(0.50)
        if ( full_width_window == True ):
            window_around = 0
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

                space_between_rooms,

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

class KWCBuildingParams:
    # TODO: docstring
    # this is getting ridiculous.
    def __init__(self,
                 building_width,
                 building_depth,
                 room_width,
                 room_height,
                 space_between_rooms,
                 window_width,
                 window_height,
                 under_window,
                 above_window,
                 around_window):
                
        self.building_width = building_width
        self.building_depth = building_depth

        self.room_width = room_width
        self.room_height = room_height

        self.space_between_rooms = space_between_rooms # space between faces

        self.window_width = window_width
        self.window_height = window_height
        self.under_window = under_window
        self.above_window = above_window
        self.around_window = around_window

# end KWCBuildingParams

class Footprint( NamedTuple ):
    footprint: list
    major_faces: list
    med_faces: list
    min_faces: list

def kwc_footprint( kwc_params: KWCParams, params: KWCBuildingParams ) -> Footprint:

    pp = pprint.PrettyPrinter( indent = 4 )

    footprint = list()

    major_faces = list()
    med_faces = list()
    min_faces = list()

    room_w = params.room_width * kwc_params.pane_w
    room_h = params.room_height * kwc_params.pane_h

    print('room width: ', room_w )

    # i just didn't want to change each one
    pane_w = kwc_params.pane_w

    # test value
    inset_between_rooms = kwc_params.pane_w * 4
    between_rooms_width = params.space_between_rooms * kwc_params.pane_w 

    #width = room_w * params.building_width + ( kwc_params.pane_w * params.space_between_rooms * ( params.building_width - 1 ) )
    #depth = room_w * params.building_depth + ( kwc_params.pane_w + params.space_between_rooms * ( params.building_depth - 1 ) )

    width = room_w * kwc_params.width + ( kwc_params.pane_w * params.space_between_rooms * ( kwc_params.width - 2 ) )
    depth = room_w * kwc_params.depth + ( kwc_params.pane_w + params.space_between_rooms * ( kwc_params.depth - 2 ) )

    print('half-width: ', width )
    print('half-depth: ', depth )

    # silly way to do this, but...
    last_vert = []

    if params.space_between_rooms > 0:
        
        marker = -0.5 * depth
        invariant = -0.5 * width 

        for i in range( 0, kwc_params.depth ):
            print("i is this", i)
            print("width  is this", kwc_params.depth )

            if i == kwc_params.depth - 1:
                print('we hit the case.')
                vert_1 = ( -0.5 * width, marker, 0 )
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )
                vert_2 = ( -0.5 * width, marker + room_w, 0 )
                footprint.append( vert_1 )
                #footprint.append( vert_2 )
                break

            vert_1 = ( -0.5 * width, marker, 0 )

            if len(last_vert) > 0:
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )

            vert_2 = ( -0.5 * width, marker + room_w, 0 )

            maj = ( vert_1, vert_2 )

            major_faces.append( maj )

            vert_3 = ( -0.5 * width + inset_between_rooms, marker + room_w, 0 )

            min_face = ( vert_2, vert_3 )
            min_faces.append( min_face )

            vert_4 = ( -0.5 * width + inset_between_rooms, marker + room_w + between_rooms_width, 0 )

            med_face = ( vert_3, vert_4 )
            med_faces.append( med_face )

            last_vert = list( vert_4 )

            marker += room_w
            marker += between_rooms_width 

            footprint.append( vert_1 )
            footprint.append( vert_2 )
            footprint.append( vert_3 )
            footprint.append( vert_4 )

        print("value of marker: ", marker )
        print("target: ", 0.5 * depth )

        marker = -0.5 * width
        invariant = 0.5 * depth

        for i in range( 0, kwc_params.width ):
            if i == kwc_params.width - 1:
                # reset our last-vert memory to nul
                print(' we hit the right case.')
                last_vert = []
                vert_1 = ( marker, invariant, 0 )
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )
                #vert_2 = ( marker + room_w, invariant, 0 )
                footprint.append( vert_1 )
                #footprint.append( vert_2 )
                break

            vert_1 = ( marker, invariant, 0 )

            if len(last_vert) > 0:
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )

            vert_2 = ( marker + room_w, invariant, 0 )

            maj = ( vert_1, vert_2 )

            major_faces.append( maj )

            vert_3 = ( marker + room_w, invariant - inset_between_rooms, 0 )

            min_face = ( vert_2, vert_3 )
            min_faces.append( min_face )

            vert_4 = ( marker + room_w + between_rooms_width, invariant - inset_between_rooms, 0 )

            med_face = ( vert_3, vert_4 )
            med_faces.append( med_face )

            last_vert = list( vert_4 )

            marker += room_w
            marker += between_rooms_width 

            footprint.append( vert_1 )
            footprint.append( vert_2 )
            footprint.append( vert_3 )
            footprint.append( vert_4 )


        #result = Footprint( footprint, major_faces, med_faces, min_faces )
        #return result 
        print('value of marker, x axis', marker )
        print('value of marker, x axis', marker )

        marker = 0.5 * depth
        invariant = 0.5 * width

        for i in range( 0, kwc_params.depth ):

            if i == kwc_params.depth - 1:
                # reset our last-vert memory to nul
                last_vert = []
                vert_1 = ( invariant, marker, 0 )
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )
                #vert_2 = ( invariant, marker - room_w, 0 )
                footprint.append( vert_1 )
                #footprint.append( vert_2 )
                break

            vert_1 = ( invariant, marker, 0 )

            if len(last_vert) > 0:
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )

            vert_2 = ( invariant, marker - room_w, 0 )

            maj = ( vert_1, vert_2 )

            major_faces.append( maj )

            vert_3 = ( invariant - inset_between_rooms, marker - room_w, 0 )

            min_face = ( vert_2, vert_3 )
            min_faces.append( min_face )

            vert_4 = ( invariant - inset_between_rooms, marker - room_w - between_rooms_width, 0 )

            med_face = ( vert_3, vert_4 )
            med_faces.append( med_face )

            last_vert = list( vert_4 )

            marker -= room_w
            marker -= between_rooms_width 

            footprint.append( vert_1 )
            footprint.append( vert_2 )
            footprint.append( vert_3 )
            footprint.append( vert_4 )


        marker = 0.5 * width 
        invariant = -0.5 * depth

        for i in range( 0, kwc_params.width ):

            if i == kwc_params.width - 1:
                # reset our last-vert memory to nul
                last_vert = []
                vert_1 = ( marker, invariant, 0 )
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )
                #vert_2 = ( marker - room_w, invariant, 0 )
                footprint.append( vert_1 )
                #footprint.append( vert_2 )
                break

            vert_1 = ( marker, invariant, 0 )

            if len(last_vert) > 0:
                min_face = ( tuple(last_vert), vert_1 )
                min_faces.append( min_face )

            vert_2 = ( marker - room_w, invariant, 0 )

            maj = ( vert_1, vert_2 )

            major_faces.append( maj )

            vert_3 = ( marker - room_w, invariant + inset_between_rooms, 0 )

            min_face = ( vert_2, vert_3 )
            min_faces.append( min_face )

            vert_4 = ( marker - room_w - between_rooms_width, invariant + inset_between_rooms, 0 )

            med_face = ( vert_3, vert_4 )
            med_faces.append( med_face )

            last_vert = list( vert_4 )

            marker -= room_w
            marker -= between_rooms_width 

            footprint.append( vert_1 )
            footprint.append( vert_2 )
            footprint.append( vert_3 )
            footprint.append( vert_4 )


        footprint.append(footprint[0])

        result = Footprint( footprint, major_faces, med_faces, min_faces )

        for j in range(0, len( footprint )):
            if footprint[j-1]:
                if footprint[j] == footprint[j-1]:
                    print("doubled verts: ", footprint[j], footprint[j-1] )
                    print("total length: ", len(footprint) )
                    print("doubled verts loca ", j, j-1 )


        pp.pprint( result )

        return result 

    fprint = list()
    major_faces = list()
    fprint.append( (-0.5 * width, -0.5 * depth, 0 ))
    fprint.append( (-0.5 * width, 0.5 * depth, 0 ))
    fprint.append( (0.5 * width, 0.5 * depth, 0 ))
    fprint.append( (0.5 * width, -0.5 * depth, 0 ))
     
    for i in range(0, len(fprint)):
        major_faces.append(fprint[i])

    result = Footprint( fprint, major_faces, [], [] )
    return result


def kwc_gen_footprint( general_params: KWCParams, params: KWCBuildingParams ) -> list:

    # in building_params, give a layout type - major faces with inset med faces in between, etc.
    # eventually return a dict with face type for each vert pair

    footprint = list()

    major_faces = list()
    med_faces = list()
    min_faces = list()

    # max 4:1 width depth ratio
    max_depth_ratio = 4

    room_w = params.room_width * general_params.pane_w
    room_h = params.room_height * general_params.pane_h

    # i just didn't want to change each one
    pane_w = general_params.pane_w

    # test value
    inset_between_rooms = general_params.pane_w * 4
    between_rooms_width = params.space_between_rooms * general_params.pane_w 

    width = room_w * params.building_width + ( general_params.pane_w * params.space_between_rooms * ( params.building_width - 1 ) )
    depth = room_w * params.building_depth + ( general_params.pane_w + params.space_between_rooms * ( params.building_depth - 1 ) )

    if params.space_between_rooms > 0:
        layout = list()

        layout.append((-0.5 * width, -0.5 * depth, 0))

        marker = -0.5 * depth
        
        #room count
        # bottom left to top left
        for face in range(0, (general_params.depth) ):
            # iterating along Y in + direction
            # don't even worry about chamfer for now.
            if marker >= 0.5 * depth:
                break

            layout.append((
                -0.5 * width,
                marker + room_w,
                0 ))

            if ( face == general_params.depth ):
                break

            layout.append((
                (-0.5 * width) + inset_between_rooms,
                marker + room_w,
                0 ))

            layout.append((
                (-0.5 * width) + inset_between_rooms,
                marker + room_w + between_rooms_width,
                0 ))

            layout.append((
                -0.5 * width,
                marker + room_w + between_rooms_width,
                0 ))

            marker += room_w 
            marker += between_rooms_width

        # top left
        
        
        layout.append((
            -0.5 * width,
            0.5 * depth,
            0 ))
        

        marker = -0.5 * width

        for face in range(0, (general_params.width - 1) ):
            # iterating along X in + direction
            # don't even worry about chamfer for now.
            if marker >= 0.5 * width:
                break

            layout.append((
                marker + room_w,
                0.5 * depth,
                0 ))

            layout.append((
                marker + room_w,
                (0.5 * depth) - inset_between_rooms,
                0 ))

            layout.append((
                marker + room_w + between_rooms_width,
                (0.5 * depth) - inset_between_rooms,
                0 ))

            layout.append((
                marker + room_w + between_rooms_width,
                (0.5 * depth),
                0 ))

            marker += room_w
            marker += between_rooms_width

        # top right
        
        layout.append((
            0.5 * width,
            0.5 * depth,
            0 ))
        

        marker = 0.5 * depth
        # right
        for face in range(0, (general_params.depth )):
            # iterating along Y in - direction
            # don't even worry about chamfer for now.
            if marker <  -0.5 * depth:
                break

            layout.append((
                0.5 * width,
                marker - room_w,
                0 ))

            if ( face == general_params.depth ):
                break

            layout.append((
                (0.5 * width) - inset_between_rooms,
                marker - room_w,
                0 ))

            layout.append((
                (0.5 * width) - inset_between_rooms,
                marker - room_w - between_rooms_width,
                0 ))

            layout.append((
                (0.5 * width),
                marker - room_w - between_rooms_width,
                0 ))

            marker -= room_w
            marker -= between_rooms_width

        # bottom right
        
        layout.append((
            0.5 * width,
            -0.5 * depth,
            0 ))
        
        
        marker = 0.5 * width

        # bottom
        for face in range(0, ( general_params.width - 1 ) ):
            # iterating along Y in + direction
            # don't even worry about chamfer for now.
            if marker <  -0.5 * width:
                break

            layout.append((
                marker - room_w,
                -0.5 * depth,
                0 ))

            layout.append((
                marker - room_w,
                (-0.5 * depth) + inset_between_rooms,
                0 ))

            layout.append((
                marker - room_w - between_rooms_width,
                (-0.5 * depth) + inset_between_rooms,
                0 ))

            layout.append((
                marker - room_w - between_rooms_width,
                (-0.5 * depth),
                0 ))

            marker -= room_w
            marker -= between_rooms_width

        layout.append( ( -0.5*width, -0.5 * depth, 0 ) )
        
        return layout



    #depth = random.randint( params.building_width, ( params.building_width * max_depth_ratio ) ) 

    # append a vert for each room boundary
    # -0.5w, iterate towards -0.5d
    # -0.5w, iterate towards 0.5d
    # 0.5d, iterate from -0.5w to 0.5w
    # 0.5w, iterate from 0.5d to -0.5d

    footprint.append( (-0.5 * width, -0.5 * depth, 0 ))
    footprint.append( (-0.5 * width, 0.5 * depth, 0 ))
    footprint.append( (0.5 * width, 0.5 * depth, 0 ))
    footprint.append( (0.5 * width, -0.5 * depth, 0 ))
    #footprint.append( (-0.5 * width, -0.5 * depth, 0 ))

    return footprint

def kwc_layout( general_params: KWCParams, kwc_params: KWCBuildingParams, footprint: list, door_position: tuple) -> dict:

    wall_loops = list()
    window_positions = list()

    # BAD variable names
    building_width = general_params.width * kwc_params.room_width
    building_depth = general_params.depth * kwc_params.room_width

    room_w = kwc_params.room_width
    room_h = kwc_params.room_height

    floor_count = random.randrange(8, 20)   # weeee
    #floor_height = 3
    floor_height = ( general_params.pane_h ) * (kwc_params.above_window + kwc_params.window_height + kwc_params.under_window )

    for i in range(0, floor_count):
        floor_print = footprint.copy()
        for j in range(0, len(floor_print) ):
            floor_print[j] = ( (footprint[j][0], footprint[j][1], floor_height * i ) )
        wall_loops.append(floor_print)

    for i in range(0, len(footprint) ):

        vert_start = footprint[i]
        if i == len(footprint) - 1:
            vert_end = footprint[0]
        else:
            vert_end = footprint[i+1]

        vec_edge = Utils.vec_from_verts( vert_end, vert_start )
        vec_0 = mathutils.Vector( (0.0, 1.0, 0.0) )
        rot = vec_edge.xy.angle_signed(vec_0.xy) - 0.5 * math.pi

        length_x = vert_end[0] - vert_start[0]
        length_y = vert_end[1] - vert_start[1]
        length = math.sqrt(length_x * length_x + length_y * length_y)

        room_count = math.floor( length / room_w )
        if room_count < 0:
            room_count = 0

        # try this
        ww_dist_x = ( room_w / length ) * length_x
        ww_dist_y = ( room_w / length ) * length_y

        print('len: ', length)
        #if math.isclose( length, building_width, rel_tol=1 ):
        print('room count: ', room_count)

        for j in range(0, room_count):
            offset = ( j * room_w ) - (0.5 * room_w)
            window_pos = ( ( vert_start[0] + ((length_x - ( room_count-1) * ww_dist_x ) / 2 ) + j*ww_dist_x),
                          ( vert_start[1] + ((length_y - ( room_count-1) * ww_dist_y ) / 2 ) + j*ww_dist_y),
                          0)
            window_positions.append((window_pos, rot))

            for floor in range(1, floor_count ):
                #pos = ( window_pos[0], window_pos[1], ( floor_height*floor ) + (kwc_params.under_window * general_params.pane_h ) )
                pos = ( window_pos[0], window_pos[1], ( floor_height*floor ))
                window_positions.append( (pos, rot) )

        '''
        if math.isclose( length, building_depth, rel_tol=1):
            print('depth axis: ', general_params.depth)
            room_count = general_params.depth

            for j in range(0, room_count):
                offset = ( j * room_w ) - (0.5 * room_w)
                window_pos = ( ( vert_start[0] + ((length_x - ( room_count-1) * ww_dist_x ) / 2 ) + j*ww_dist_x),
                              ( vert_start[1] + ((length_y - ( room_count-1) * ww_dist_y ) / 2 ) + j*ww_dist_y),
                              0)
                window_positions.append((window_pos, rot))
        
        else:
            print('poo poo pee pee')
        '''

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


