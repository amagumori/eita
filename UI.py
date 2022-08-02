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

from bpy.types import Panel, PropertyGroup
from bpy.props import FloatProperty, BoolProperty, EnumProperty, IntProperty


class PBGPropertyGroup(PropertyGroup):
    # TODO: docstring

    building_width : FloatProperty(
        name="Building width",
        default=25.0
    )

    building_depth : FloatProperty(
        name="Building depth",
        default=15.0
    )

    building_chamfer : FloatProperty(
        name="Chamfer size",
        default=1
    )

    building_wedge_depth : FloatProperty(
        name="Wedge depth",
        default=1.5
    )

    building_wedge_width : FloatProperty(
        name="Wedge width",
        default=8
    )

    floor_first_offset : FloatProperty(
        name="FIrst floor offset",
        default=0.7
    )

    floor_height : FloatProperty(
        name="Floor height",
        default=3
    )

    floor_count : IntProperty(
        name="Number of floors",
        default=2
    )

    floor_separator_include : BoolProperty(
        name="Separator between floors",
        default=True
    )

    floor_separator_height : FloatProperty(
        name="Separator height",
        default=0.2
    )

    floor_separator_width : FloatProperty(
        name="Separator width",
        default=0.2
    )

    window_width : FloatProperty(
        name="Total window width",
        default=1.2
    )

    distance_window_window : FloatProperty(
        name="Distance between windows",
        default=2.5
    )

    generate_pillar : BoolProperty(
        name="Generate Pillar",
        default=True
    )

    distance_window_pillar : FloatProperty(
        name="Distance Window to Pillar",
        default=0.8
    )

    pillar_width : FloatProperty(
        name="Pillar width",
        default=0.2
    )

    pillar_depth : FloatProperty(
        name="Pillar depth",
        default=0.15
    )

    pillar_chamfer : FloatProperty(
        name="Pillar Chamfer",
        default=0.05
    )

    pillar_offset_height : FloatProperty(
        name="Pillar Offset Height",
        default=0.7
    )

    pillar_offset_size : FloatProperty(
        name="Pillar Offset Size",
        default=0.05
    )

    pillar_include_floor_separator : BoolProperty(
        name="Include floor separator",
        default=True
    )

    pillar_include_first_floor : BoolProperty(
        name="Include first floor",
        default=True
    )

    wall_types = [
        ("FLAT", "FLAT", "", 0),
        ("ROWS", "ROWS", "", 1)
    ]

    wall_type : EnumProperty(
        items=wall_types,
        default="ROWS"
    )

    wall_mortar_size : FloatProperty(
        name="Mortar size",
        default=0.01
    )

    wall_section_size : FloatProperty(
        name="Brick section size",
        default=0.02
    )

    wall_row_count : IntProperty(
        name="Rows per floor",
        default=7
    )

    wall_offset_size : FloatProperty(
        name="Wall offset size",
        default=0.1
    )

    wall_offset_type : EnumProperty(
        items=wall_types,
        default="ROWS"
    )

    wall_offset_mortar_size : FloatProperty(
        name="Offset Mortar size",
        default=0.02
    )

    wall_offset_section_size : FloatProperty(
        name="Offset Brick section size",
        default=0.03
    )

    wall_offset_row_count : IntProperty(
        name="Offset Rows per floor",
        default=3
    )

    window_height : FloatProperty(
        name="Window total height",
        default=1.7
    )

    window_offset : FloatProperty(
        name="Window offset",
        default=0.7
    )

    window_under_types = [
        ("WALL", "WALL", "", 0),
        ("PILLARS", "PILLARS", "", 1),
        ("SIMPLE", "SIMPLE", "", 2),
        ("SINE", "SINE", "", 3),
        ("CYCLOID", "CYCLOID", "", 4)
    ]

    windows_under_type : EnumProperty(
        items=window_under_types,
        default="WALL"
    )

    windows_under_width : FloatProperty(
        name="under window offset width",
        default=0.1
    )

    windows_under_height : FloatProperty(
        name="Under Window offset height",
        default=0.1
    )

    windows_under_depth : FloatProperty(
        name="under Window offset depth",
        default=0.05
    )

    windows_under_inset_depth : FloatProperty(
        name="under Window inset depth",
        default=0.1
    )

    windows_under_amplitude : FloatProperty(
        name="under Window amplitude",
        default=0.05
    )

    windows_under_period_count : IntProperty(
        name="under Window period count",
        default=8
    )

    windows_under_simple_width : FloatProperty(
        name="Under window simple width",
        default=0.04
    )

    windows_under_simple_depth : FloatProperty(
        name="Under window simple depth",
        default=0.03
    )

    windows_under_pillar_base_diameter : FloatProperty(
        name="Under window pillar base diameter",
        default=0.08
    )

    windows_under_pillar_base_height : FloatProperty(
        name="Under window pillar base height",
        default=0.04
    )

    windows_under_pillar_min_diameter : FloatProperty(
        name="Under window pillar min diameter",
        default=0.05
    )

    windows_under_pillar_max_diameter : FloatProperty(
        name="Under window pillar max diameter",
        default=0.08
    )

    window_above_types = [
        ("WALL", "WALL", "", 0),
        ("SIMPLE", "SIMPLE", "", 1),
        ("SINE", "SINE", "", 2),
        ("CYCLOID", "CYCLOID", "", 3)
    ]

    windows_above_type : EnumProperty(
        items=window_above_types,
        default="WALL"
    )

    windows_above_width : FloatProperty(
        name="under window offset width",
        default=0.1
    )

    windows_above_height : FloatProperty(
        name="Under Window offset height",
        default=0.1
    )

    windows_above_depth : FloatProperty(
        name="under Window offset depth",
        default=0.05
    )

    windows_above_inset_depth : FloatProperty(
        name="under Window inset depth",
        default=0.1
    )

    windows_above_amplitude : FloatProperty(
        name="under Window amplitude",
        default=0.05
    )

    windows_above_period_count : IntProperty(
        name="under Window period count",
        default=8
    )

    windows_above_simple_width : FloatProperty(
        name="Under window simple width",
        default=0.04
    )

    windows_above_simple_depth : FloatProperty(
        name="Under window simple depth",
        default=0.03
    )

    stairs_layout_width : FloatProperty(
        name="Stairs width",
        default=9.0
    )

    stairs_layout_depth : FloatProperty(
        name="Stairs depth",
        default=2.0
    )

    stairs_stair_count : IntProperty(
        name="stair count",
        default=4
    )

    stairs_width : FloatProperty(
        name="stair width",
        default=0.25
    )

    windows_around_section_height : FloatProperty(
        name="Window around section height",
        default=0.15
    )

    windows_around_section_width : FloatProperty(
        name="Window around section width",
        default=0.1
    )

    windows_around_pillar_width : FloatProperty(
        name="Window around pillar width",
        default=0.1
    )

    windows_around_inner_depth : FloatProperty(
        name="Window around inner depth",
        default=0.05
    )

    windows_around_outer_depth : FloatProperty(
        name="Window around outer depth",
        default=0.03
    )

    window_frame_width : FloatProperty(
        name="Window frame width",
        default=0.03
    )

    window_frame_depth : FloatProperty(
        name="Window frame depth",
        default=0.03
    )

    window_ratio : FloatProperty(
        name="Window ratio",
        default=0.7
    )

    window_count : IntProperty(
        name="window count",
        default=2
    )

    window_grid : BoolProperty(
            name="grid window?",
            default=False
    )

    window_simple_section : BoolProperty(
            name="simple section type",
            default=False
    )

    window_split_top : BoolProperty(
        name="window split top",
        default=False
    )

    roof_offset_width : FloatProperty(
        name="roof offset width",
        default=4.0
    )

    roof_offset_wedge : FloatProperty(
        name="roof offset wedge",
        default=7.5
    )

    roof_height : FloatProperty(
        name="roof height",
        default=3.0
    )

    door_width : FloatProperty(
        name="Door width",
        default=2.0
    )

    door_height : FloatProperty(
        name="Door height",
        default=2.5
    )

    door_around_section_height : FloatProperty(
        name="Door around section height",
        default=0.2
    )

    door_around_section_width : FloatProperty(
        name="Door around section width",
        default=0.15
    )

    door_around_pillar_width : FloatProperty(
        name="Door around pillar width",
        default=0.15
    )

    door_around_inner_depth : FloatProperty(
        name="Door around inner depth",
        default=0.1
    )

    door_around_outer_depth : FloatProperty(
        name="Door around outer depth",
        default=0.03
    )

    door_spacing : FloatProperty(
        name="Door spacing",
        default=0.1
    )

    door_count_x : IntProperty(
        name="Door count x",
        default=2
    )

    door_count_z : IntProperty(
        name="Door count x",
        default=5
    )

    door_block_depth : FloatProperty(
        name="Door block depth",
        default=0.07
    )

    door_block_width : FloatProperty(
        name="Door block width",
        default=0.05
    )

# end PBGPropertyGroup


class PBGToolbarGeneralPanel(Panel):
    # TODO: docstring
    bl_label = "General Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Overall Building Dimensions")
        col.prop(properties, "building_width")
        col.prop(properties, "building_depth")
        col.prop(properties, "building_chamfer")
        col.prop(properties, "building_wedge_depth")
        col.prop(properties, "building_wedge_width")

        col.label(text="Floor and separator layout")
        col.prop(properties, "floor_count")
        col.prop(properties, "floor_height")
        col.prop(properties, "floor_first_offset")
        col.prop(properties, "floor_separator_include")
        col.prop(properties, "floor_separator_width")
        col.prop(properties, "floor_separator_height")
    # end draw
# end PBGToolbarPanel


class PBGToolbarLayoutPanel(Panel):
    # TODO: docstring
    bl_label = "Layout Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.prop(properties, "distance_window_window")
        col.prop(properties, "distance_window_pillar")
    # end draw
# end PBGLayoutPanel


class PBGToolbarPillarPanel(Panel):
    # TODO: docstring
    bl_label = "Pillar Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.prop(properties, "generate_pillar")
        col.prop(properties, "pillar_width")
        col.prop(properties, "pillar_depth")
        col.prop(properties, "pillar_chamfer")
        col.prop(properties, "pillar_offset_height")
        col.prop(properties, "pillar_offset_size")
        col.prop(properties, "pillar_include_floor_separator")
        col.prop(properties, "pillar_include_first_floor")
    # end draw
# end PBGPillarPanel


class PBGToolbarWallPanel(Panel):
    # TODO: docstring
    bl_label = "Wall settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Wall settings")
        col.prop(properties, "wall_type")
        col.prop(properties, "wall_mortar_size")
        col.prop(properties, "wall_section_size")
        col.prop(properties, "wall_row_count")

        col.label(text="First floor offset settings")
        col.prop(properties, "wall_offset_size")
        col.prop(properties, "wall_offset_type")
        col.prop(properties, "wall_offset_mortar_size")
        col.prop(properties, "wall_offset_section_size")
        col.prop(properties, "wall_offset_row_count")
    # end draw
# end PBGToolbarWallPanel


class PBGToolbarWindowPanel(Panel):
    bl_label = "Window Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Overall window dimensions")
        col.prop(properties, "window_width")
        col.prop(properties, "window_height")
        col.prop(properties, "window_offset")
        col.label(text="Around windows")
        col.prop(properties, "windows_around_section_height")
        col.prop(properties, "windows_around_section_width")
        col.prop(properties, "windows_around_pillar_width")
        col.prop(properties, "windows_around_inner_depth")
        col.prop(properties, "windows_around_outer_depth")
        col.label(text="window frame")
        col.prop(properties, "window_frame_width")
        col.prop(properties, "window_frame_depth")
        col.prop(properties, "window_ratio")
        col.prop(properties, "window_count")
        col.prop(properties, "window_split_top")
        #
        col.prop(properties, "window_grid")
        col.prop(properties, "window_simple_section")
    # end draw
# end PBGToolbarWindowPanel


class PBGToolbarWindowUnderPanel(Panel):
    bl_label = "Window Under Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup
        col = layout.column(align=True)
        col.label(text="OOverall dimensions")
        col.prop(properties, "windows_under_type")
        col.prop(properties, "windows_under_width")
        col.prop(properties, "windows_under_height")
        col.prop(properties, "windows_under_depth")
        col.prop(properties, "windows_under_inset_depth")

        col.label(text="Sine/Cycloid params")
        col.prop(properties, "windows_under_amplitude")
        col.prop(properties, "windows_under_period_count")

        col.label(text="Simple params")
        col.prop(properties, "windows_under_simple_width")
        col.prop(properties, "windows_under_simple_depth")

        col.label(text="Pillar params")
        col.prop(properties, "windows_under_pillar_base_diameter")
        col.prop(properties, "windows_under_pillar_base_height")
        col.prop(properties, "windows_under_pillar_min_diameter")
        col.prop(properties, "windows_under_pillar_max_diameter")
    # end draw
# end PBGToolbarWindowPanel


class PBGToolbarWindowAbovePanel(Panel):
    bl_label = "Window Above Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Overall dimensions")
        col.prop(properties, "windows_above_type")
        col.prop(properties, "windows_above_width")
        col.prop(properties, "windows_above_height")
        col.prop(properties, "windows_above_depth")
        col.prop(properties, "windows_above_inset_depth")

        col.label(text="Sine/Cycloid params")
        col.prop(properties, "windows_above_amplitude")
        col.prop(properties, "windows_above_period_count")

        col.label(text="Simple params")
        col.prop(properties, "windows_above_simple_width")
        col.prop(properties, "windows_above_simple_depth")
    # end draw
# end PBGToolbarWindowPanel


class PBGToolbarStairsPanel(Panel):
    bl_label = "Stairs Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Stairs settings")
        col.prop(properties, "stairs_layout_width")
        col.prop(properties, "stairs_layout_depth")
        col.prop(properties, "stairs_stair_count")
        col.prop(properties, "stairs_width")
    # end draw
# end PBGToolbarStairsPanel


class PBGToolbarRoofPanel(Panel):
    bl_label = "Roof Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Roof settings")
        col.prop(properties, "roof_offset_width")
        col.prop(properties, "roof_offset_wedge")
        col.prop(properties, "roof_height")
    # end draw
# end PBGToolbarRoofPanel


class PBGToolbarDoorPanel(Panel):
    bl_label = "Door Settings"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.PBGPropertyGroup

        col = layout.column(align=True)
        col.label(text="Door settings")
        col.prop(properties, "door_width")
        col.prop(properties, "door_height")
        col.label(text="Around Door")
        col.prop(properties, "door_around_section_height")
        col.prop(properties, "door_around_section_width")
        col.prop(properties, "door_around_pillar_width")
        col.prop(properties, "door_around_inner_depth")
        col.prop(properties, "door_around_outer_depth")
        col.label(text="Doors")
        col.prop(properties, "door_spacing")
        col.prop(properties, "door_count_x")
        col.prop(properties, "door_count_z")
        col.prop(properties, "door_block_width")
        col.prop(properties, "door_block_depth")
    # end draw
# end PBGToolbarDoorPanel


class PBGToolbarGeneratePanel(Panel):
    # TODO: docstring
    bl_label = "Generate"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator("pbg.generate_building", text="Generate")
    # end draw
# end PBGGeneratePanel

class PBGToolbarMyGeneratePanel(Panel):
    bl_label="peepee poopoo"
    bl_category=""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator("pbg.my_generate_building", text="Bruh")
    # end draw
# end PBGMyGeneratePanel
