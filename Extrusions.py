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

# square profile in XY
# x is width, y is depth
def square_section_mesh( width, height ) -> list:
    verts = list()
    verts.append( (-0.5 * width, -0.5 * depth, 0 ) )
    verts.append( (-0.5 * width, 0.5 * depth, 0 ) )
    verts.append( (0.5 * width, 0.5 * depth, 0 ) )
    verts.append( (0.5 * width, -0.5 * depth, 0 ) )
 
    edges = list()
    i = 0
    while i < len(square)-1:
        edges.append([i, i+1]),
        i += 1
    # end while

    m = bpy.data.meshes.new(name="SquareSection")
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

def square_pillar( thickness, edge ) -> bpy.types.Mesh:

    sq = square_section_mesh( thickness, thickness )

    GenUtils.extrude_along_edge( sq, edge, False )
