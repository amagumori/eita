import bmesh
import bpy
import mathutils
import math
import pprint
from . import Utils
from . import GenUtils
from . import GenLayout
from . import GenMesh

from . import NewLayout

class KWCWindows:

    def __init__(self):
        print('foo')
            # end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.KWCPropertyGroup
        params = ParamsWindows(
            properties.pane_w,
            properties.pane_h
            )
        return params
    # end from_ui
# end KWCWindows

class ParamsWindowCage:
    def __init__(self,
                 cage_type: str,
                 width: float,
                 height: float,
                 spacing_vertical: float,      # spacing of vertical bars
                 spacing_horizontal: float,    # spacing OF horizontal bars
                 depth:  float,      # how far it comes out from window, better term?
                 bar_thickness: float,  # bar dia / width
                 bar_profile: str,      # square / round bar
                 row_type: str,         # evenly spaced or ratio rows..placeholder
                 row_ratio: float ):

        self.type = cage_type
        self.width = width
        self.height = height
        self.spacing_horizontal = spacing_horizontal
        self.spacing_vertical = spacing_vertical
        self.depth = depth
        self.bar_thickness = bar_thickness
        self.bar_profile = bar_profile
        self.row_type = row_type
        self.row_ratio = row_ratio

    #end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsWindowCage(
                properties.window_cage_type,
                properties.window_cage_width,
                properties.window_cage_height,
                properties.window_cage_spacing_vert,
                properties.window_cage_spacing_horiz,
                properties.window_cage_depth,
                properties.window_cage_bar_thickness,
                properties.window_cage_bar_profile,
                properties.window_cage_row_type,
                properties.window_cage_row_ratio
        )
        return params
    # end from_ui
# end ParamsWindowCage

'''
    layout_vertical.append((-0.5 * params_cage.width, -params_cage.depth, 0.0))
    layout_vertical.append((-0.5 * params_cage.width, params_cage.depth, 0.0))
    layout_vertical.append((0.5 * params_cage.width, params_cage.depth, 0.0))
    layout_vertical.append((0.5 * params_cage.width, -params_cage.depth, 0.0))

    layout_horizontal = list()

    
    layout_horizontal.append((-0.5 * params_cage.height, -params_cage.depth, 0.0))
    layout_horizontal.append((-0.5 * params_cage.height, params_cage.depth, 0.0))
    layout_horizontal.append((0.5 * params_cage.height, params_cage.depth, 0.0))
    layout_horizontal.append((0.5 * params_cage.height, -params_cage.depth, 0.0))
    '''

# when generating footprint, store a dict of
#   vert pairs : maj / med / min enum

def kwc_gen_mesh_windows_maj(context: bpy.types.Context, 
                             kwc_params: NewLayout.KWCParams,
                             kwc_building_params: NewLayout.KWCBuildingParams ):
                             
                             #kwc_window_params: KWCWindowParams ):

    pane_w = kwc_params.pane_w
    pane_h = kwc_params.pane_h

    bm = bmesh.new()

    window_width = kwc_building_params.maj_window_width * pane_w
    window_height = kwc_building_params.maj_window_height * pane_h
           
    # create section
    params = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
    if params_windows.simple_section == True:
        sequence = GenUtils.gen_simple_section_list( params_windows.section_width, params_windows.section_height)
    else:
        sequence = GenUtils.gen_section_element_list(params)

    m_section = GenUtils.gen_section_mesh(sequence, kwc_building_params.maj_window_width, kwc_window_params.window_depth )
    
    bm_section = bmesh.new()
    bm_section.from_mesh(m_section)
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    mat_rot = mathutils.Matrix.Rotation(math.radians(-90), 3, "X")

    vec_trans = (0.0, -kwc_building_params.window_width, 0.0)

    bmesh.ops.rotate(bm_section, cent=(0, 0, 0), matrix=mat_rot, verts=bm_section.verts, space=mat_loc)
    bmesh.ops.translate(bm_section, vec=vec_trans, space=mat_loc, verts=bm_section.verts)
    bm_section.to_mesh(m_section)
    bm_section.free()

    # generate single layout for top and bottom, check for splits here
    layout_top = list()
    layout_bottom = list()
    m_bottom_glass = bpy.data.meshes.new("KWCWindowBottomGlass")
    m_top_glass = bpy.data.meshes.new("KWCWindowTopGlass")
    verts_bottom_glass = list()
    verts_top_glass = list()
    #

    if kwc_window_params.grid == True:

        layout = list()
        m_grid_glass = bpy.data.meshes.new("WindowGridGlass")
        verts_grid_glass = list()

        layout.append( (0.5*maj_window_width, 0, 0 ) ) 
        layout.append( (0.5*maj_window_width - pane_w, 0, 0 ) ) 
        layout.append( (0.5*maj_window_width - pane_w, pane_h, 0 ) )
        layout.append( (0.5*maj_window_width, pane_h, 0 ) )

        print('layout: ', layout)

        verts_grid_glass.append((layout[0][0] - window_width,
                                 layout[0][1] + window_width, 0.0))
        verts_grid_glass.append((layout[1][0] + window_width,
                                 layout[1][1] + window_width, 0.0))
        verts_grid_glass.append((layout[2][0] + window_width,
                                 layout[2][1] - window_width, 0.0))
        verts_grid_glass.append((layout[3][0] - window_width,
                                 layout[2][1] - window_width, 0.0))

        print(verts_grid_glass)

        m_grid_glass.from_pydata( verts_grid_glass, [(0,1), (1,2), (2,3), (3,0)], [(0, 1, 2, 3)])
        m_grid = Utils.extrude_along_edges(m_section.copy(), layout, True)

        bm.from_mesh(m_grid_glass)
        for face in bm.faces:
            face.material_index = 1
        bm.from_mesh(m_grid)

        
        geom_orig = bm.verts[:] + bm.edges[:] + bm.faces[:]

        for i in range(1, kwc_building_params.window_width):
            ret_dup = bmesh.ops.duplicate(bm, geom=geom_orig)
            verts_to_translate_x = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            mat_loc = mathutils.Matrix.Translation((0.0,0.0,0.0))
            vec_width_trans = ( -pane_w * i, 0, 0)
            bmesh.ops.translate(bm, vec=vec_width_trans, verts=verts_to_translate_x, space=mat_loc)
        # lol bumbo coder moment
        geom_orig = bm.verts[:] + bm.edges[:] + bm.faces[:]

        for i in range(1, kwc_building_params.window_height):
            dup = bmesh.ops.duplicate(bm, geom=geom_orig)
            verts = [ele for ele in dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
            mat_loc = mathutils.Matrix.Translation((0.0,0.0,0.0))
            vec_height_trans = ( 0, pane_h * i, 0 )
            bmesh.ops.translate(bm, vec=vec_height_trans, verts=verts, space=mat_loc)

        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))

        # inner_depth - depth of window from wall
        # window_offset - distance from window to floor
        # section height - height of window-frame-section

        # translate "in" by inner_depth and "up" by windowoffset+section_height
        window_inset = 0.05
        from_bottom = pane_y * kwc_building_params.maj_under_window 
        vec_trans = (0.0, -window_inset, from_bottom)
        #vec_trans = (0.0, -window_inset, params_general.window_offset + params_windows.section_height)
        mat_rot = mathutils.Matrix.Rotation(math.radians(90), 3, "X")
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mat_rot, verts=bm.verts, space=mat_loc)
        bmesh.ops.translate(bm, vec=vec_trans, space=mat_loc, verts=bm.verts)

        # create object
        m = bpy.data.meshes.new("KWCWindow")
        bm.to_mesh(m)
        bm.free()
        ob = bpy.data.objects.get("KWCWindow")
        if ob is not None:
            #context.scene.objects.unlink(ob)
            bpy.data.objects.remove(ob)

        # link the created object to the scene
        new_obj = bpy.data.objects.new("KWCWindow", m)
        context.scene.collection.objects.link(new_obj)
        return new_obj

    # just do split top with a single row on top, no ratio or nothing
    if kwc_window_params.split_top == True:
        
        layout_top.append((0.5 * maj_window_width, frame_height - pane_y, 0))
        layout_top.append((0.5 * maj_window_width - pane_w, maj_window_height - pane_y, 0))
        layout_top.append((0.5 * maj_window_width - pane_w, maj_window_height, 0))
        layout_top.append((0.5 * maj_window_width, frame_height, 0))
        
    else:

        layout_top.append((0.5 * maj_window_width, frame_height * params_windows.window_ratio, 0))
        layout_top.append((-0.5 * maj_window_width, frame_height * params_windows.window_ratio, 0))
        layout_top.append((-0.5 * maj_window_width, frame_height, 0))
        layout_top.append((0.5 * maj_window_width, frame_height, 0))

    layout_bottom.append((0.5*maj_window_width, 0, 0))
    layout_bottom.append((0.5*maj_window_width - frame_window_width, 0, 0))
    layout_bottom.append((0.5*maj_window_width - frame_window_width, frame_height*params_windows.window_ratio, 0))
    layout_bottom.append((0.5*maj_window_width, frame_height*params_windows.window_ratio, 0))

    # create glass
    verts_top_glass.append((layout_top[0][0] - window_width,
                            layout_top[0][1] + window_width, 0.0))
    verts_top_glass.append((layout_top[1][0] + window_width,
                            layout_top[1][1] + window_width, 0.0))
    verts_top_glass.append((layout_top[2][0] + window_width,
                            layout_top[2][1] - window_width, 0.0))
    verts_top_glass.append((layout_top[3][0] - window_width,
                            layout_top[2][1] - window_width, 0.0))

    verts_bottom_glass.append((layout_bottom[0][0] - window_width,
                               layout_bottom[0][1] + window_width, 0.0))
    verts_bottom_glass.append((layout_bottom[1][0] + window_width,
                               layout_bottom[1][1] + window_width, 0.0))
    verts_bottom_glass.append((layout_bottom[2][0] + window_width,
                               layout_bottom[2][1] - window_width, 0.0))
    verts_bottom_glass.append((layout_bottom[3][0] - window_width,
                               layout_bottom[2][1] - window_width, 0.0))

    m_top_glass.from_pydata(verts_top_glass, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])
    m_bottom_glass.from_pydata(verts_bottom_glass, [(0, 1), (1, 2), (2, 3), (3, 0)], [(0, 1, 2, 3)])

    # extrude along layouts
    m_bottom = Utils.extrude_along_edges(m_section.copy(), layout_bottom, True)
    m_top = Utils.extrude_along_edges(m_section, layout_top, True)

    bm.from_mesh(m_bottom_glass)
    for face in bm.faces:
        face.material_index = 1
    bm.from_mesh(m_bottom)

    if params_windows.split_top == True:
        faces_to_exclude = bm.faces[:]
        bm.from_mesh(m_top_glass)
        for face in bm.faces:
            if face not in faces_to_exclude:
                face.material_index = 1
        bm.from_mesh(m_top)

    # duplicate and translate frames
    geom_orig = bm.verts[:] + bm.edges[:] + bm.faces[:]
    for i in range(1, params_windows.window_count):
        ret_dup = bmesh.ops.duplicate(bm, geom=geom_orig)
        verts_to_translate = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        vec_trans = (-frame_window_width*i, 0, 0)
        bmesh.ops.translate(bm, vec=vec_trans, verts=verts_to_translate, space=mat_loc)

    if params_windows.split_top == False:
        faces_to_exclude = bm.faces[:]
        bm.from_mesh(m_top_glass)
        for face in bm.faces:
            if face not in faces_to_exclude:
                face.material_index = 1
        bm.from_mesh(m_top)

    # rotate window, move on z
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    vec_trans = (0.0, -params_windows.inner_depth, params_general.window_offset + params_windows.section_height)
    mat_rot = mathutils.Matrix.Rotation(math.radians(90), 3, "X")
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mat_rot, verts=bm.verts, space=mat_loc)
    bmesh.ops.translate(bm, vec=vec_trans, space=mat_loc, verts=bm.verts)

    # create object
    m = bpy.data.meshes.new("KWCWindow")
    bm.to_mesh(m)
    bm.free()
    ob = bpy.data.objects.get("KWCWindow")
    if ob is not None:
        #context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)

    # link the created object to the scene
    new_obj = bpy.data.objects.new("KWCWindow", m)
    context.scene.collection.objects.link(new_obj)
    return new_obj
# end gen_mesh_windows

def gen_wall( context: bpy.types.Context,
              footprint: list,
              section_mesh: bpy.types.Mesh ) -> bpy.types.Object:
    
    bm = bmesh.new()
    mesh = Utils.extrude_along_edges( section_mesh.copy(), footprint, False )
    bm.from_mesh(mesh)

    m = bpy.data.meshes.new( "footprintExtrusionTest" )
    bm.to_mesh(m)
    bm.free()

    obj = bpy.data.objects.new("footprintTest", m)
    context.collection.objects.link(obj)
    return obj


def gen_mesh_window_cage( context: bpy.types.Context,
                          params_cage: ParamsWindowCage,
                          params_window: GenMesh.ParamsWindows,
                          params_general: GenLayout.ParamsGeneral ) -> bpy.types.Object:
    """
    """

    bm = bmesh.new()

    bar_section_list = GenUtils.gen_simple_section_list(params_cage.bar_thickness, params_cage.bar_thickness )
    bar_section_mesh = GenUtils.gen_section_mesh(bar_section_list, params_cage.bar_thickness, params_cage.bar_thickness)

    layout_vertical  = list()
    
    layout_vertical.append((-0.5 * params_general.window_width, -params_cage.depth, 0.0))
    layout_vertical.append((-0.5 * params_general.window_width, params_cage.depth, 0.0))
    layout_vertical.append((0.5 * params_general.window_width, params_cage.depth, 0.0))
    layout_vertical.append((0.5 * params_general.window_width, -params_cage.depth, 0.0))

    layout_horizontal = list()

    layout_horizontal.append((-0.5 * params_general.window_height, -params_cage.depth, 0.0))
    layout_horizontal.append((-0.5 * params_general.window_height, params_cage.depth, 0.0))
    layout_horizontal.append((0.5 * params_general.window_height, params_cage.depth, 0.0))
    layout_horizontal.append((0.5 * params_general.window_height, -params_cage.depth, 0.0))
    
    m = Utils.extrude_along_edges(bar_section_mesh, layout_vertical, False)

    bm.from_mesh(m)
    geo = bm.verts[:] + bm.edges[:] + bm.faces[:]
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    #steps = int( params_cage.height // params_cage.spacing_vertical )
    steps = int( params_general.window_height // params_cage.spacing_vertical )
    print( "STEPS - VERTICAL ", steps )
    bmesh.ops.spin(
            bm,
            geom=geo,
            cent=(0.0,0.0,0.0),
            axis=(0.0,0.0,0.0),
            dvec=(0.0,0.0,params_cage.spacing_vertical),
            angle=0.0,
            space=mat_loc,
            steps=steps,
            use_merge=False,
            use_normal_flip=False,
            use_duplicate=True)

    another_sec =  GenUtils.gen_section_mesh(bar_section_list, params_cage.bar_thickness, params_cage.bar_thickness)
    mesh = Utils.extrude_along_edges(another_sec, layout_horizontal, False)

    bmosh = bmesh.new()

    bmosh.from_mesh(mesh)

    vts = bmosh.verts[:]
    rot_mat = mathutils.Matrix.Rotation( math.radians( 90 ), 4, 'Y')
    bmesh.ops.rotate(bmosh,
            cent=(0.0,0.0,0.0),
            matrix=rot_mat,
            verts=vts,
            space=mat_loc,
            use_shapekey=False)
    

    geo = bmosh.verts[:] + bmosh.edges[:] + bmosh.faces[:]
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    steps = int( params_general.window_width // params_cage.spacing_horizontal )
    print( "STEPS - HORIZONTAL - ", steps )
    bmesh.ops.spin(
            bmosh,
            geom=geo,
            cent=(0.0,0.0,0.0),
            axis=(0.0,0.0,0.0),
            dvec=(params_cage.spacing_horizontal, 0.0, 0.0 ),
            angle=0.0,
            space=mat_loc,
            steps=steps,
            use_merge=False,
            use_normal_flip=False,
            use_duplicate=True)

    vts = bmosh.verts[:]
    bmesh.ops.translate( bmosh,
            vec=( -0.5*params_general.window_width, 0.0, 0.5*params_general.window_height),
            space=mat_loc,
            verts=vts,
            use_shapekey=False)
   
    mtwo = bpy.data.meshes.new("windowCageBarVertical")
    bmosh.to_mesh(mtwo)
    bmosh.free()
    #new_obj_two = bpy.data.objects.new("windowCageBarVertical", mtwo)
    #context.scene.collection.objects.link(new_obj_two)
    
    bm.from_mesh( mtwo )
    
    vts = bm.verts[:]
    bmesh.ops.translate( bm,
            vec=( 0.0, 0.0, params_general.window_offset ),
            space=mat_loc,
            verts=vts,
            use_shapekey=False)

    m = bpy.data.meshes.new("windowCageBar")
    bm.to_mesh(m)
    bm.free()

    new_obj = bpy.data.objects.new("windowCageBar", m)
    context.scene.collection.objects.link(new_obj)
    return new_obj


class ParamsAwning:
    def __init__(self,
                 width: float,
                 depth_from_wall: float, # how much it sticks out from wall
                 spacing_x: float,      # use these to generate rows / cols
                 spacing_y: float,
                 depth:  float,      # how far it comes out from window, better term?
                 bar_thickness: float,  # bar dia / width
                 bar_profile: str,      # square / round bar
                 row_type: str,         # evenly spaced or ratio rows..placeholder
                 row_ratio: float,      # ''
                 cage_type:  str):       # diagonal / horizontal bars

        self.type = cage_type
        self.width = width
        self.height = height
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.depth = depth
        self.bar_thickness = bar_thickness
        self.bar_profile = bar_profile
        self.row_type = row_type
        self.row_ratio = row_ratio

    #end __init__

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.PBGPropertyGroup
        params = ParamsWindowCage(
                properties.window_cage_type,
                properties.window_cage_width,
                properties.window_cage_height,
                properties.window_cage_spacing_x,
                properties.window_cage_spacing_y,
                properties.window_cage_depth,
                properties.window_cage_bar_thickness,
                properties.window_cage_bar_profile,
                properties.window_cage_type,
                properties.window_cage_row_type,
                properties.window_cage_row_ratio
        )
        return params
    # end from_ui
# end ParamsWindowCage

def gen_awning_from_footprint() -> bpy.types.Mesh:

    awning_profile_list = GenUtils.gen_awning_section_list(25, 3, 1, 0.03)
    awning_profile = GenUtils.gen_plane_profile( awning_profile_list, width )


def gen_balcony_section () -> bpy.types.Mesh:
    """
    Generates a mesh from the given list of sectionElements.

    Args:
         sequence (list of SectionElement): a list of SectionElements, to be used for generating the mesh. Likely the
             result of calling the generate_section function.
         height (float): height of the section
         width (float): width of the section

    Returns, bpy.types.Mesh:
        A mesh following the sequence, in Y-Z plane, starting in (0,0,0), with width and height of 1 blender unit.
    """

    width = 1 
    height = 1 

    thickness = 0.05
    balcony_depth = 2
    chamfer = 0.03
    balcony_height = 0.6


    verts = list()
    verts.append([0, 0, 0])

    verts.append([0, balcony_depth, 0])
    verts.append([0, balcony_depth, balcony_height - (0.5*chamfer) ])
    verts.append([0, balcony_depth - (0.5*chamfer), balcony_height ])
    verts.append([0, verts[-1][1] - thickness, balcony_height ])
    verts.append([0, verts[-1][1], thickness ]) #bottom inner vert 
    verts.append([0, 0, thickness ])


    edges = list()
    i = 0
    while i < len(verts)-1:
        edges.append([i, i+1]),
        i += 1
    # end while

    m = bpy.data.meshes.new(name="TestBalcony")
    m.from_pydata(verts, edges, [])
    m.update()
    bm = bmesh.new()
    bm.from_mesh(m)

    # scale the mesh so it has the desired width and height.
    mat_loc = mathutils.Matrix.Translation((0, 0, 0))
    bmesh.ops.scale(bm, vec=(1.0, width, height), space=mat_loc, verts=bm.verts)

    bm.to_mesh(m)
    bm.free()
    return m
# end generate_section_mesh

def gen_balcony(context: bpy.types.Context, 
                footprint: list,
                section_mesh: bpy.types.Mesh,
                is_loop: bool ) -> bpy.types.Object:
    """
        Creates the floor separator object
        floor separator will be placed at the origin (0, 0, 0)
    Args:
        context: bpy.types.Context
        footprint: list(tuple(x,y,z)) - building footprint
        section_mesh: cross section/side profile of the separator
    Returns:
        bpy.types.Object - single separator object placed at origin
    """

    # extrude the section along the footprint to create the separator
    m = Utils.extrude_along_edges(section_mesh, footprint, is_loop)

    # create a new object, link it to the scene and return it
    obj = bpy.data.objects.new("beppBalcony", m)
    context.collection.objects.link(obj)
    return obj
# end gen_mesh_floor_separator

def gen_window_balcony(context: bpy.types.Context, 
        section_mesh: bpy.types.Mesh, width ) -> bpy.types.Object:
    
    edge = list()

    first_vert = list()

    first_vert = ((
        0.5 * width,
        0.0,
        0.0 ))
    second_vert = list()
    second_vert = ((
        -0.5 * width,
        0.0,
        0.0 ))
    edge.append( first_vert )
    edge.append( second_vert )

    # extrude the section along the footprint to create the separator
    m = Utils.extrude_along_edges(section_mesh, edge, False)

    # create a new object, link it to the scene and return it
    obj = bpy.data.objects.new("windowBalcony", m)
    context.collection.objects.link(obj)
    return obj
# end gen_mesh_floor_separator

def gen_window_awning ( context: bpy.types.Context, params_general: GenLayout.ParamsGeneral ) -> bpy.types.Object:
    awning_profile_list = GenUtils.gen_awning_section_list( params_general.window_width,
                                                            0.05,
                                                            0.05,
                                                            0.05 )

    awning_profile = GenUtils.gen_plane_profile( awning_profile_list, params_general.window_width )

    section = bmesh.new()
    section.from_mesh( awning_profile )

    mat_loc = mathutils.Matrix.Translation( ( 0.0, 0.0, 0.0 ) )
    depth = 1
    down = 0.2

    geo = bmesh.ops.extrude_edge_only( section,
            edges= section.edges[:],
            use_normal_flip=False,
            use_select_history=False )
   
    verts_to_translate = [ele for ele in geo["geom"] if isinstance(ele, bmesh.types.BMVert)]

    bmesh.ops.translate( section,
            vec=(depth, 0.0, 0.0),
            space=mat_loc,
            verts=verts_to_translate,
            use_shapekey=False )

    mat_rot = mathutils.Matrix.Rotation( math.radians( -90 ), 3, "Z" )

    vts = section.verts[:]

    bmesh.ops.rotate( section,
            cent=(0,0,0),
            matrix = mat_rot,
            verts = vts,
            space= mat_loc,
            use_shapekey = False )

    slope_rot = mathutils.Matrix.Rotation( math.radians( -15 ), 3, "X" )

    bmesh.ops.rotate( section,
            cent=(0,0,0),
            matrix = slope_rot,
            verts = vts,
            space= mat_loc,
            use_shapekey = False )

    #vts = section.verts[:]

    bmesh.ops.translate( section,
            vec= ( -params_general.window_width, depth, 0.0 ),
            space= mat_loc,
            verts= vts,
            use_shapekey= False )
    

    m = bpy.data.meshes.new('test_awning')
    section.to_mesh( m )
    section.free()

    obj = bpy.data.objects.new( "window_awning", m )
    context.scene.collection.objects.link( obj )

    return obj

def get_edges_from_window_positions( context: bpy.types.Context, params: GenLayout.ParamsGeneral, window_positions: list ) -> list:
    edges = list()

    # need to build edges first in same plane as windows
    # then move to window_pos + rot

    for loc in window_positions:
        pprint.pprint(loc[1])
        edge = list()

        first_vert = list()

        first_vert = ((
            0.5 * params.window_width,
            0.5 * params.window_width,
            #0.0,
            0.0 ))
        second_vert = list()
        second_vert = ((
            -0.5 * params.window_width,
            -0.5* params.window_width,
            #0.0,
            0.0 ))

        '''
        first_vert = ((
            loc[0][0] + 0.5 * params.window_width,
            loc[0][1],
            loc[0][2] ))
        second_vert = list()
        second_vert = ((
            loc[0][0] - 0.5 * params.window_width,
            loc[0][1],
            loc[0][2] ))
        '''
        
        
        vec0 = mathutils.Vector( (first_vert[0], first_vert[1], first_vert[2]) )
        vec1 = mathutils.Vector( (second_vert[0], second_vert[1], second_vert[2]) )

        myvec = vec1 - vec0
        z_vec = mathutils.Vector( (0.0,0.0,1.0) )

        norm = myvec.cross(z_vec)
        norm.normalize()

        vec_edge = Utils.vec_from_verts(second_vert, first_vert)
        vec_0 = mathutils.Vector((0.0, 1.0, 0.0))
        rot = vec_edge.xy.angle_signed(vec_0.xy) - 0.5 * math.pi

        mat = mathutils.Matrix.Rotation( math.radians(loc[1]), 4, (0,0,1) )
        euler = mathutils.Euler( (0.0, 0.0, 0.0) )
        euler.z = rot + math.pi
        vec0.rotate( euler )
        vec1.rotate( euler )

        second_vert = ( vec1.x, vec1.y, vec1.z )
        first_vert = ( vec0.x, vec0.y, vec0.z )
        

        edge.append( second_vert )
        edge.append( first_vert )
        edges.append(edge)


    return edges

def gen_balcony_from_loops(context: bpy.types.Context, 
                loops: list,
                section_mesh: bpy.types.Mesh ) -> bpy.types.Object:
    
    bm = bmesh.new()
    for loop in loops:
        mesh = Utils.extrude_along_edges( section_mesh.copy(), loop, False )
        bm.from_mesh(mesh)

    m = bpy.data.meshes.new( "windowBalcony")
    bm.to_mesh(m)
    bm.free()

    # create a new object, link it to the scene and return it
    obj = bpy.data.objects.new("beppBalcony", m)
    context.collection.objects.link(obj)
    return obj

