import bmesh
import bpy
import mathutils
import math
import pprint
from . import Utils
from . import GenUtils
from . import GenLayout

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

def gen_mesh_window_cage( context: bpy.types.Context,
                          params_cage: ParamsWindowCage,
                          params_general: GenLayout.ParamsGeneral ) -> bpy.types.Object:
    """
    """

    bm = bmesh.new()

    bar_section_list = GenUtils.gen_simple_section_list(params_cage.bar_thickness, params_cage.bar_thickness )
    bar_section_mesh = GenUtils.gen_section_mesh(bar_section_list, params_cage.bar_thickness, params_cage.bar_thickness)

    layout_vertical  = list()

    layout_vertical.append((-0.5 * params_cage.width, -params_cage.depth, 0.0))
    layout_vertical.append((-0.5 * params_cage.width, params_cage.depth, 0.0))
    layout_vertical.append((0.5 * params_cage.width, params_cage.depth, 0.0))
    layout_vertical.append((0.5 * params_cage.width, -params_cage.depth, 0.0))

    layout_horizontal = list()

    
    layout_horizontal.append((-0.5 * params_cage.height, -params_cage.depth, 0.0))
    layout_horizontal.append((-0.5 * params_cage.height, params_cage.depth, 0.0))
    layout_horizontal.append((0.5 * params_cage.height, params_cage.depth, 0.0))
    layout_horizontal.append((0.5 * params_cage.height, -params_cage.depth, 0.0))
   
    m = Utils.extrude_along_edges(bar_section_mesh, layout_vertical, False)

    bm.from_mesh(m)
    geo = bm.verts[:] + bm.edges[:] + bm.faces[:]
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    steps = int( params_cage.height // params_cage.spacing_vertical )
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
    steps = int( params_cage.width // params_cage.spacing_horizontal )
    
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
            vec=( -0.5*params_cage.width, 0.0, 0.5*params_cage.height),
            space=mat_loc,
            verts=vts,
            use_shapekey=False)
   
    mtwo = bpy.data.meshes.new("windowCageBarVertical")
    bmosh.to_mesh(mtwo)
    bmosh.free()
    new_obj_two = bpy.data.objects.new("windowCageBarVertical", mtwo)
    context.scene.collection.objects.link(new_obj_two)
    

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
        -0.5 * width,
        0.0,
        0.0 ))
    second_vert = list()
    second_vert = ((
        0.5 * width,
        0.0,
        0.0 ))
    edge.append( second_vert )
    edge.append( first_vert )

    # extrude the section along the footprint to create the separator
    m = Utils.extrude_along_edges(section_mesh, edge, False)

    # create a new object, link it to the scene and return it
    obj = bpy.data.objects.new("windowBalcony", m)
    context.collection.objects.link(obj)
    return obj
# end gen_mesh_floor_separator


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
            0.0,
            0.0 ))
        second_vert = list()
        second_vert = ((
            -0.5* params.window_width,
            0.0,
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
        
        '''
        vec0 = mathutils.Vector( (first_vert[0], first_vert[1], first_vert[2]) )
        vec1 = mathutils.Vector( (second_vert[0], second_vert[1], second_vert[2]) )

        myvec = vec1 - vec0
        z_vec = mathutils.Vector( (0.0,0.0,1.0) )

        norm = myvec.cross(z_vec)
        norm.normalize()

        mat = mathutils.Matrix.Rotation( math.radians(loc[1]), 4, (0,0,1) )
        #euler = mathutils.Euler( (0.0, 0.0, math.radians(loc[1]) ) )
        eul = mathutils.Euler( (0.0,0.0,0.0) )
        eul.z = loc[1] + ( 0.5 * math.pi )
        vec0.rotate( eul )
        vec1.rotate( eul )

        first_vert = ( vec0.x, vec0.y, vec0.z )
        second_vert = ( vec1.x, vec1.y, vec1.z )
        '''

        edge.append( first_vert )
        edge.append( second_vert )
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

