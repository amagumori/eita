import bmesh
import bpy
import mathutils
import math
from . import Utils
from . import GenUtils
from . import GenLayout

class ParamsWindowCage:
    def __init__(self,
                 cage_type: str,
                 width: float,
                 height: float,
                 spacing_x: float,      # use these to generate rows / cols
                 spacing_y: float,
                 depth:  float,      # how far it comes out from window, better term?
                 bar_thickness: float,  # bar dia / width
                 bar_profile: str,      # square / round bar
                 row_type: str,         # evenly spaced or ratio rows..placeholder
                 row_ratio: float ):

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

    bar_spacing_x = params_cage.width / params_cage.spacing_x 
    bar_spacing_y = params_cage.height / params_cage.spacing_y

    vertical = list()
    horiz = list()

    test = list()
    test.append( (0.0, 0.0, 0.0 ) ) 
    test.append( (params_cage.height, 0.0, 0.0 ) )
   
    layout = list()

    '''
    layout.append((-0.5 * params_cage.depth, params_cage.height, 0.0))
    layout.append((-0.5 * params_cage.depth, 0.0, 0.0))
    layout.append((0.5 * params_cage.depth, -params_cage.height, 0.0))
    layout.append((0.5 * params_cage.depth, -params_cage.height, 0.0))
    '''

    layout.append((-0.5 * params_cage.height, -params_cage.depth, 0.0))
    layout.append((-0.5 * params_cage.height, params_cage.depth, 0.0))
    layout.append((0.5 * params_cage.height, params_cage.depth, 0.0))
    layout.append((0.5 * params_cage.height, -params_cage.depth, 0.0))

    #XZ - width height
    #Y -  depth
    
    '''
    vertical.append( (0.0,0.0,0.0) )
    vertical.append( (0.0, params_cage.depth, 0.0 ) )
    vertical.append( (0.0, params_cage.depth, params_cage.height ) )
    vertical.append( (0.0, 0.0, params_cage.height ) ) 
    '''

    vertical.append( (0.0, 0.0, params_cage.height ) ) 
    vertical.append( (0.0, params_cage.depth, params_cage.height ) )
    vertical.append( (0.0, params_cage.depth, 0.0 ) )

    m = Utils.extrude_along_edges(bar_section_mesh, layout, False)
    bm.from_mesh(m)
    geo = bm.verts[:] + bm.edges[:] + bm.faces[:]
    mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
    steps = int( params_cage.width // params_cage.spacing_x )
    bmesh.ops.spin(
            bm,
            geom=geo,
            cent=(0.0,0.0,0.0),
            axis=(0.0,0.0,0.0),
            dvec=(0.0,0.0,params_cage.spacing_x),
            angle=0.0,
            space=mat_loc,
            steps=steps,
            use_merge=False,
            use_normal_flip=False,
            use_duplicate=True)


    '''
    i=0
    while i < params_cage.width:
        print('i: ', i)
        print('spacing x by i', params_cage.spacing_x*i )
        trans = mathutils.Matrix.Translation((0.0, 0.0, params_cage.spacing_x * i ) )

        geom_to_duplicate = bm.verts[:] + bm.edges[:] + bm.faces[:]
        #ret_dup = bmesh.ops.duplicate(bm, geom=geom_to_duplicate)

        bpy.ops.mesh.duplicate_move(geom_to_duplicate, (0.0,0.0,params_cage.spacing_x*i))

        #verts_to_transform = [ele for ele in ret_dup["geom"] if isinstance(ele, bmesh.types.BMVert)]
        #mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        #bmesh.ops.translate(bm, vec=(0.0, 0.0, params_cage.spacing_x * i ), verts=verts_to_transform, space=mat_loc)

        i += params_cage.spacing_x
    '''

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


