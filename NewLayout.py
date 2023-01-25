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
            #print("i is this", i)
            #print("width  is this", kwc_params.depth )

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


        pp.pprint( major_faces )

        result = Footprint( footprint, major_faces, med_faces, min_faces )

        for j in range(0, len( footprint )):
            if footprint[j-1]:
                if footprint[j] == footprint[j-1]:
                    print("doubled verts: ", footprint[j], footprint[j-1] )
                    print("total length: ", len(footprint) )
                    print("doubled verts loca ", j, j-1 )



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

def kwc_layout( general_params: KWCParams, kwc_params: KWCBuildingParams, fprint: Footprint, door_position: tuple) -> dict:

    footprint = fprint.footprint
    major_faces = fprint.major_faces

    wall_loops = list()
    window_positions = list()

    # BAD variable names
    building_width = general_params.width * kwc_params.room_width
    building_depth = general_params.depth * kwc_params.room_width

    pane_w = general_params.pane_w 
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


    # major faces loop
    for i in range(0, len( major_faces ) ):
        edge = major_faces[i]
        vert_start = edge[0]
        vert_end = edge[-1]

        vec_edge = Utils.vec_from_verts( vert_end, vert_start )
        vec_0 = mathutils.Vector( (0.0, 1.0, 0.0) )
        rot = vec_edge.xy.angle_signed( vec_0.xy ) - 0.5 * math.pi

        x_len = vert_end[0] - vert_start[0]
        y_len = vert_end[1] - vert_start[1]
        length = math.sqrt( x_len * x_len + y_len * y_len )

        ww_x = ( ( kwc_params.window_width / 2 ) * general_params.pane_w ) * x_len 
        ww_y = ( ( kwc_params.window_width / 2 )  * general_params.pane_w ) * y_len

        x_term = x_len * (room_w/2)
        y_term = y_len * (room_w/2)

        offset_x = ( room_w * general_params.pane_w) * x_len 
        offset_y = ( room_w * general_params.pane_w ) * y_len 
        half_window = kwc_params.window_width * general_params.pane_w 
        print('x: ', ( ww_x / 4 ) )
        print('y:', ( ww_y / 4 ) )
        #x = vert_start[0] + ( ww_x  / 4 ) 
        #y = vert_start[1] + ( ww_y / 4 ) 

        x = vert_start[0] + ( x_len / 2 )  
        y = vert_start[1] + ( y_len / 2 ) 

        window_pos = ( ( x, y, 0 ) )
        window_positions.append( (window_pos, rot) )

        for floor in range( 0, floor_count ):
            pos = ( window_pos[0], window_pos[1], ( floor_height * floor ) )
            window_positions.append( (pos, rot) )


    '''
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

'''
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

'''
