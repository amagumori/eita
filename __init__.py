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
import importlib

#from . import UI
#from . import Generator


bl_info = {
    "name": "EITA",
    "description": "Proceduraly generate and edit buildings",
    "author": "Luka Šimić",
    "version": (0, 8, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Toolbox > PBG",
    "warning": "Under development. Might cause stability issues.",
    "wiki_url": "https://github.com/lsimic/ProceduralBuildingGenerator/wiki",
    "tracker_url": "https://github.com/lsimic/ProceduralBuildingGenerator/issues",
    "support": "COMMUNITY",
    "category": "Add Mesh"
}

if "UI" in locals():
    importlib.reload(UI)
if "Generator" in locals():
    importlib.reload(Generator)
if "MyGenerator" in locals():
    importlib.reload(MyGenerator)
if "GenMesh" in locals():
    importlib.reload(GenMesh)
if "NewMesh" in locals():
    importlib.reload(NewMesh)
if "NewLayout" in locals():
    importlib.reload(NewLayout)
if "GenLayout" in locals():
    importlib.reload(GenLayout)
if "GenUtils" in locals():
    importlib.reload(GenUtils)
if "Constants" in locals():
    importlib.reload(Constants)

from . import UI
from . import Generator

def register():

    bpy.utils.register_class(UI.KWCPropertyGroup)
    bpy.utils.register_class(UI.KWCPanel)
    bpy.types.Scene.KWCPropertyGroup = bpy.props.PointerProperty(type=UI.KWCPropertyGroup)

    bpy.utils.register_class(UI.PBGPropertyGroup)
    bpy.types.Scene.PBGPropertyGroup = bpy.props.PointerProperty(type=UI.PBGPropertyGroup)
    #

    bpy.utils.register_class(Generator.FootprintTest)
    bpy.utils.register_class(UI.WindowCageDebugPanel)
    bpy.utils.register_class(UI.PBGToolbarTestFootprint)

    bpy.utils.register_class( UI.FacePropertyGroup )
    bpy.utils.register_class( UI.FootprintPropertyGroup )

    bpy.types.Scene.FootprintPropertyGroup = bpy.props.PointerProperty(type=UI.FootprintPropertyGroup)

    bpy.types.Scene.FacePropertyGroup = bpy.props.PointerProperty(type=UI.FacePropertyGroup)

    bpy.utils.register_class( UI.NewFootprintPanel )

    #
    bpy.utils.register_class(UI.PBGToolbarGeneralPanel)
    bpy.utils.register_class(UI.PBGToolbarLayoutPanel)
    bpy.utils.register_class(UI.PBGToolbarPillarPanel)
    bpy.utils.register_class(UI.PBGToolbarWallPanel)
    bpy.utils.register_class(UI.PBGToolbarWindowPanel)
    bpy.utils.register_class(UI.PBGToolbarWindowAbovePanel)
    bpy.utils.register_class(UI.PBGToolbarWindowUnderPanel)
    bpy.utils.register_class(UI.PBGToolbarStairsPanel)
    bpy.utils.register_class(UI.PBGToolbarRoofPanel)
    bpy.utils.register_class(UI.PBGToolbarDoorPanel)
    bpy.utils.register_class(UI.PBGToolbarGeneratePanel)
    ##
    bpy.utils.register_class(Generator.MyGenerator)
    bpy.utils.register_class(Generator.Generator)


def unregister():
    del bpy.types.Scene.PBGPropertyGroup
    del bpy.types.Scene.FootprintPropertyGroup
    del bpy.types.Scene.FacePropertyGroup 
    del bpy.types.Scene.KWCPropertyGroup

    bpy.utils.unregister_class(UI.KWCPropertyGroup)
    bpy.utils.unregister_class(UI.KWCPanel)

    bpy.utils.unregister_class(UI.PBGPropertyGroup)
    #
    bpy.utils.unregister_class(UI.WindowCageDebugPanel)
    bpy.utils.unregister_class(Generator.FootprintTest)

    bpy.utils.unregister_class( UI.FacePropertyGroup )
    bpy.utils.unregister_class( UI.FootprintPropertyGroup )

    bpy.utils.unregister_class( UI.NewFootprintPanel )

    bpy.utils.unregister_class(UI.PBGToolbarGeneralPanel)
    bpy.utils.unregister_class(UI.PBGToolbarLayoutPanel)
    bpy.utils.unregister_class(UI.PBGToolbarPillarPanel)
    bpy.utils.unregister_class(UI.PBGToolbarWallPanel)
    bpy.utils.unregister_class(UI.PBGToolbarWindowPanel)
    bpy.utils.unregister_class(UI.PBGToolbarWindowAbovePanel)
    bpy.utils.unregister_class(UI.PBGToolbarWindowUnderPanel)
    bpy.utils.unregister_class(UI.PBGToolbarStairsPanel)
    bpy.utils.unregister_class(UI.PBGToolbarRoofPanel)
    bpy.utils.unregister_class(UI.PBGToolbarDoorPanel)
    bpy.utils.unregister_class(UI.PBGToolbarGeneratePanel)
    ##
    bpy.utils.unregister_class(UI.PBGToolbarTestFootprint)
    bpy.utils.unregister_class(Generator.MyGenerator)
    ##
    bpy.utils.unregister_class(Generator.Generator)
