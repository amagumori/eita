# implementing simple square footprints first.

# putting this here for now
class KWCBuildingParams:
    # TODO: docstring
    # this is getting ridiculous.
    def __init__(self,
                 maj_room_width,
                 maj_room_height,
                 maj_window_width,
                 maj_window_height,
                 maj_under_window,
                 maj_above_window,
                 maj_around_window,

                 med_room_width,
                 med_room_height,
                 med_window_width,
                 med_window_height,
                 med_under_window,
                 med_above_window,
                 med_around_window,

                 min_room_width,
                 min_room_height,
                 min_window_width,
                 min_window_height,
                 min_under_window,
                 min_above_window,
                 min_around_window):

        self.maj_room_width = maj_room_width
        self.maj_room_height = maj_room_height
        self.maj_under_window = maj_under_window
        self.maj_above_window = maj_above_window
        self.maj_around_window = maj_around_window

        self.med_room_width = med_room_width
        self.med_room_height = med_room_height
        self.med_under_window = med_under_window
        self.med_above_window = med_above_window
        self.med_around_window = med_around_window

        self.min_room_width = min_room_width
        self.min_room_height = min_room_height
        self.min_under_window = min_under_window
        self.min_above_window = min_above_window
        self.min_around_window = min_around_window

# end KWCBuildingParams


def kwc_gen_layout( kwc_params: KWCLayoutParams, params_general: ParamsGeneral, footprint: list, door_position: tuple) -> dict:
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

        # divide by "window unit" width
        window_count = length / kwc_params.width
        window_width_x = (kwc_params.width / length) * length_x
        window_width_y = (kwc_params.width / length) * length_y

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


        ww_dist_x = kwc_params.width
        ww_dist_y = kwc_params.width

        for j in range(0, window_count):
            # calculate window position
            window_pos = ((vert_start[0] + ((length_x - (window_count - 1) * ww_dist_x) / 2) + j * ww_dist_x),
                          (vert_start[1] + ((length_y - (window_count - 1) * ww_dist_y) / 2) + j * ww_dist_y),
                          params_general.floor_offset
                          )

            # check whether the window intersects with the door, push first floor accordingly
            vert_1 = (window_pos[0] - 0.5 * window_width_x, window_pos[1] - 0.5 * window_width_y, 0)
            vert_2 = (window_pos[0] + 0.5 * window_width_x, window_pos[1] - 0.5 * window_width_y, 0)

            window_loop = list()
            window_positions.append( (window_pos, rot) )

            """
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
            """

            # push all other floors
            for floor in range(1, params_general.floor_count + 1):
                pos = (window_pos[0], window_pos[1], params_general.floor_offset + floor * params_general.floor_height)
                window_positions.append((pos, rot))
            # end for

            """
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
            """

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
#

"""
