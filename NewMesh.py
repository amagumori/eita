import bmesh
import bpy
import mathutils
import math
from . import Utils
from . import GenUtils
from . import GenLayout

class ParamsWindowCage:
    def __init__(self,
                 width: float,
                 height: float,
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

def gen_mesh_window_cage( context: bpy.types.Context,
                          params_cage: ParamsWindowCage,
                          params_general: GenLayout.ParamsGeneral ) -> bpy.types.Object:
    """
    """

    bm = bmesh.new()

    bar_spacing_x = window_cage_width / window_cage_spacing_x
    bar_spacing_y = window_cage_height / window_cage_spacing_y


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


