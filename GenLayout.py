# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Procedural building generator
#  Copyright (C) 2019 Luka Simic
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import math
import mathutils
from . import Utils


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
    def __init__(self, building_width, building_depth, building_chamfer, building_wedge_depth, building_wedge_width, front_face_inset_from_edge, front_face_inset_depth, front_face_inset_chamfer):
        self.building_width = building_width
        self.building_depth = building_depth
        self.building_chamfer = building_chamfer
        self.building_wedge_depth = building_wedge_depth
        self.building_wedge_width = building_wedge_width

        self.front_face_inset_from_edge = front_face_inset_from_edge
        self.front_face_inset_depth = front_face_inset_depth 
        self.front_face_inset_chamfer = front_face_inset_chamfer  
    # end init

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsFootprint(
            building_width=properties.building_width,
            building_depth=properties.building_depth,
            building_chamfer=properties.building_chamfer,
            building_wedge_depth=properties.building_wedge_depth,
            building_wedge_width=properties.building_wedge_width,
            front_face_inset_from_edge=properties.front_face_inset_from_edge,
            front_face_inset_depth=properties.front_face_inset_depth,
            front_face_inset_chamfer=properties.front_face_inset_chamfer
        )
        return params
    # end from_ui
# end ParamsFootprint

# we will maybe want in the future gen nonstandard footprint
# can build more complicated arbitrary-poly footprints, etc.

# @TODO also need to implement gen_internal_walls and gen_internal_floors.

def gen_footprint(params_footprint: ParamsFootprint) -> list:
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

    layout = list()
    # bottom left corner
    if params_footprint.building_chamfer > 0:
        layout.append((-0.5 * params_footprint.building_width + params_footprint.building_chamfer,
                       -0.5 * params_footprint.building_depth, 0))
        layout.append((-0.5 * params_footprint.building_width,
                       -0.5 * params_footprint.building_depth + params_footprint.building_chamfer, 0))
    else:
        layout.append((-0.5 * params_footprint.building_width, -0.5 * params_footprint.building_depth, 0))

    # top left corner
    if params_footprint.building_chamfer > 0:
        layout.append((-0.5 * params_footprint.building_width,
                       0.5 * params_footprint.building_depth - params_footprint.building_chamfer, 0))
        layout.append((-0.5 * params_footprint.building_width + params_footprint.building_chamfer,
                       0.5 * params_footprint.building_depth, 0))
    else:
        layout.append((-0.5 * params_footprint.building_width, 0.5 * params_footprint.building_depth, 0))

    # wedge
    if params_footprint.building_wedge_depth > 0 and params_footprint.building_wedge_width > 0:
        layout.append((-0.5 * params_footprint.building_wedge_width, 0.5 * params_footprint.building_depth, 0))
        layout.append((-0.5 * params_footprint.building_wedge_width,
                       0.5 * params_footprint.building_depth + params_footprint.building_wedge_depth, 0))
        layout.append((0.5 * params_footprint.building_wedge_width,
                       0.5 * params_footprint.building_depth + params_footprint.building_wedge_depth, 0))
        layout.append((0.5 * params_footprint.building_wedge_width, 0.5 * params_footprint.building_depth, 0))

    # top right corner
    if params_footprint.building_chamfer > 0:
        layout.append((0.5 * params_footprint.building_width - params_footprint.building_chamfer,
                       0.5 * params_footprint.building_depth, 0))
        layout.append((0.5 * params_footprint.building_width,
                       0.5 * params_footprint.building_depth - params_footprint.building_chamfer, 0))
    else:
        layout.append((0.5 * params_footprint.building_width, 0.5 * params_footprint.building_depth, 0))

    # bottom right corner
    if params_footprint.building_chamfer > 0:
        layout.append((0.5 * params_footprint.building_width,
                       -0.5 * params_footprint.building_depth + params_footprint.building_chamfer, 0))
        layout.append((0.5 * params_footprint.building_width - params_footprint.building_chamfer,
                       -0.5 * params_footprint.building_depth, 0))
    else:
        layout.append((0.5 * params_footprint.building_width, -0.5 * params_footprint.building_depth, 0))

    # return the list
    return layout
# end gen_footprint

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

def pick_out_balcony_edges ( footprint: list, params: ParamsFootprint, balcony_type: str ) -> list:
    balcony = list()
    
    if balcony_type == 'front_and_sides_wraparound':
        # then you really just take the existing footprint????
        # back building face is fixed up in wall_loops routine
        # this works as intended...
        # footprint.append( footprint[0] )
        balcony.append( footprint[1:-1] )
        return footprint

    if balcony_type == 'front_only':
        if params.building_chamfer > 0:
            balcony.append( footprint[3] )
            balcony.append( footprint[4] )
            return balcony
            # and that's our edge - excluding chamfer
        else:
            # one vertex per corner, starting bottom left.
            balcony.append( footprint[1] )
            balcony.append( footprint[2] )
            return balcony

    #if balcony_type == 'all_sides':

def gen_layout(params_general: ParamsGeneral, footprint: list, door_position: tuple) -> dict:
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
            "pillar_positions" - list(tuple(tuple(x,y,z), rot)) list of tuples, where each item contains the x,y,z
                position of the pillar and it's rotation on the z axis.
            wall_loops - list(list(tuple(x,y,z)) - list, containing a list of verts, ie loops to be used for extruding
                walls
    """
    window_positions = list()
    pillar_positions = list()
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
            wall_verts_initial.append((vert_start[0], vert_start[1], params_general.floor_offset))
        else:
            wall_verts.append((vert_start[0], vert_start[1], params_general.floor_offset))
        # end if;

        # calculate length of edge
        length_x = vert_end[0] - vert_start[0]
        length_y = vert_end[1] - vert_start[1]
        length = math.sqrt(length_x * length_x + length_y * length_y)

        # calculate number of windows for this edge
        if params_general.generate_pillar:
            window_count = math.floor((length - 2 * params_general.distance_window_pillar) /
                                      params_general.distance_window_window) + 1
        else:
            window_count = math.floor((length - params_general.window_width) /
                                      params_general.distance_window_window) + 1

        # sanity check here
        if window_count < 0:
            window_count = 0

        # calculate distance between windows on x and y axis
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

        # calculate window and pillar rotation (it's always the same)
        vec_edge = Utils.vec_from_verts(vert_end, vert_start)
        vec_0 = mathutils.Vector((0.0, 1.0, 0.0))
        rot = vec_edge.xy.angle_signed(vec_0.xy) - 0.5 * math.pi

        # calculate door range for calculating intersects
        door_size_x = math.cos(door_position[1])*params_general.door_width
        door_size_y = math.sin(door_position[1])*params_general.door_width
        door_start = (door_position[0][0]-0.5*door_size_x,
                      door_position[0][1]-0.5*door_size_y,
                      params_general.floor_offset)
        door_end = (door_position[0][0]+0.5*door_size_x,
                    door_position[0][1]+0.5*door_size_y,
                    params_general.floor_offset)
        for j in range(0, window_count):
            # calculate window position
            window_pos = ((vert_start[0] + ((length_x - (window_count - 1) * ww_dist_x) / 2) + j * ww_dist_x),
                          (vert_start[1] + ((length_y - (window_count - 1) * ww_dist_y) / 2) + j * ww_dist_y),
                          params_general.floor_offset
                          )

            # check whether the window intersects with the door, push first floor accordingly
            vert_1 = (window_pos[0] - 0.5 * window_width_x, window_pos[1] - 0.5 * window_width_y, 0)
            vert_2 = (window_pos[0] + 0.5 * window_width_x, window_pos[1] - 0.5 * window_width_y, 0)
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
                    window_loop.append((vert_2[0], vert_2[1], params_general.floor_offset))
                    wall_loops.append(window_loop)
                elif(Utils.vert_check_intersect(vert_2, door_start, door_end) and
                     (not Utils.vert_check_intersect(vert_1, door_start, door_end))):
                    window_loop = list()
                    window_loop.append((vert_1[0], vert_1[1], params_general.floor_offset))
                    window_loop.append(door_start)
                    wall_loops.append(window_loop)
                elif(Utils.vert_check_intersect(window_pos, door_start, door_end) and
                     (not Utils.vert_check_intersect(vert_1, door_start, door_end)) and
                     (not Utils.vert_check_intersect(vert_1, door_start, door_end))):
                    window_loop = list()
                    window_loop.append((vert_1[0], vert_1[1], params_general.floor_offset))
                    window_loop.append(door_start)
                    wall_loops.append(window_loop)
                    window_loop = list()
                    window_loop.append(door_end)
                    window_loop.append((vert_2[0], vert_2[1], params_general.floor_offset))
                    wall_loops.append(window_loop)
            # end if

            # push all other floors
            for floor in range(1, params_general.floor_count + 1):
                pos = (window_pos[0], window_pos[1], params_general.floor_offset + floor * params_general.floor_height)
                window_positions.append((pos, rot))
            # end for

            # calculate pillar position
            if j == 0 or has_single_pillar is False:
                pillar_pos = (
                    window_pos[0] - wp_dist_x,
                    window_pos[1] - wp_dist_y,
                    params_general.floor_offset
                )

                # check whether the pillar intersects with the door, push accordingly
                if not Utils.vert_check_intersect(pillar_pos, door_start, door_end):
                    pillar_positions.append((pillar_pos, rot))
                # end if

                # push all other floors
                for floor in range(1, params_general.floor_count+1):
                    pos = (pillar_pos[0], pillar_pos[1], params_general.floor_offset+floor*params_general.floor_height)
                    pillar_positions.append((pos, rot))
                # end for
            # end if
            pillar_pos = (
                window_pos[0] + wp_dist_x,
                window_pos[1] + wp_dist_y,
                params_general.floor_offset
            )

            # check whether the pillar intersects with the door, push accordingly
            if not Utils.vert_check_intersect(pillar_pos, door_start, door_end):
                pillar_positions.append((pillar_pos, rot))
            # end if

            # push all other floors
            for floor in range(1, params_general.floor_count + 1):
                pos = (pillar_pos[0], pillar_pos[1], params_general.floor_offset + floor * params_general.floor_height)
                pillar_positions.append((pos, rot))
            # end for

            # calculate the last vert of this loop, because it is broken by the window
            vert_wall = (window_pos[0] - 0.5 * window_width_x,
                         window_pos[1] - 0.5 * window_width_y,
                         params_general.floor_offset)
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
                for floor in range(1, params_general.floor_count + 1):
                    loop = list()
                    for vert in wall_verts:
                        loop.append((vert[0], vert[1], params_general.floor_offset + floor*params_general.floor_height))
                    wall_loops.append(loop)
                wall_verts.clear()
            # end if

            # calculate the first vert of the next loop and push it into the loops array
            vert_wall = (window_pos[0] + 0.5 * window_width_x,
                         window_pos[1] + 0.5 * window_width_y,
                         params_general.floor_offset)
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

            # make a copy of wall_verts for each floor, push for each floor except ground
            for floor in range(1, params_general.floor_count + 1):
                loop = list()
                for vert in verts:
                    loop.append((vert[0], vert[1], params_general.floor_offset + floor * params_general.floor_height))
                wall_loops.append(loop)
            wall_verts.clear()
        # end if
    # end for

    # put all results in a dictionary and return it
    result = {
        "window_positions": window_positions,
        "pillar_positions": pillar_positions,
        "wall_loops": wall_loops
    }
    return result
# end generate_vertical_layout
