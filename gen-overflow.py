
class FaceParams:
    def __init__(self, 
                 face_type,
                 room_width,
                 room_height,
                 window_width,
                 window_height,
                 under_window,
                 above_window,
                 around_window):

        self.face_type = face_type
        self.room_width = room_width
        self.room_height = room_height
        self.window_width = window_height
        self.under_window = under_window
        self.above_window = above_window
        self.around_window = around_window

#end FaceParams

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
    # this is getting ridiculous.
    def __init__(self, left, bottom, right, top, building_width, building_depth):

        self.building_width = building_width
        self.building_depth = building_depth
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.FootprintPropertyGroup
        params = ParamsFootprint(
            building_width=properties.building_width,
            building_depth=properties.building_depth,
            left=properties.left,
            top=properties.top,
            right=properties.right,
            bottom=properties.bottom
        )
        return params
    # end from_ui
# end ParamsFootprint

class ParamsFootprintFace:
    # TODO: docstring
    def __init__(self, face_type, inset_first_floor):
        
        # chamfers and broad bldg params need to be passed in 
        # to not fuck everything

        # eventually we will stack footprints for different
        # building profiles
        # "bridge_loops" API will be used to bridge bottom footprint loop
        # to top one.

        #self.curved_corner = curved_corner # bool
        #self.corner_chamfer = corner_chamfer
        #self.corner_radius = corner_radius # work on this later.

        self.face_type = face_type # major, med, minor

        # doing the inset stuff per side.
        #self.ff_inset = inset_first_floor  # bool
        #self.ff_from_edge = inset_first_floor_d_from_edge
        #self.ff_inset_depth = inset_first_floor_depth
        #self.ff_inset_chamfer = inset_first_floor_chamfer

        self.subface_count = subface_count
        self.subface_offset = subface_offset
        self.subface_depth = subface_depth # can be negative and outset
        self.subface_width = subface_width

    # end init

    @staticmethod
    def from_ui():
        properties = bpy.context.scene.FacePropertyGroup
        params = ParamsFootprintFace(

            #curved_corner = properties.curved_corner, # bool
            #corner_chamfer = properties.corner_chamfer
            #corner_radius = corner_radius, # work on this later.

            face_type = properties.face_type,
            
            #ff_inset = properties.inset_first_floor,  # bool
            #ff_from_edge = properties.inset_first_floor_d_from_edge,
            #ff_inset_depth = properties.inset_first_floor_depth,
            #ff_inset_chamfer = properties.inset_first_floor_chamfer,

            subface_count = properties.subface_count,
            subface_offset = properties.subface_offset,
            subface_depth = properties.subface_depth, # can be negative
            subface_width = properties.subface_width,

        )
        return params


"""
class KWCGenerator(bpy.types.Operator):
    bl_idname = "pbg.generate_kowloon"
    bl_label = "generate kwc building"

    def invoke(self, context, event):
        group = bpy.data.collections.get("kwc_group")
        if not group:
            bpy.ops.collection.create(name="kwc_group")
            group = bpy.data.collections.get("kwc_group")
        # delete all objects from group
        for obj in group.objects:
            bpy.data.objects.remove(obj)
        
        params_kwc = NewLayout.KWCLayoutParams.from_ui()
        #params_section = GenUtils.ParamsSectionFactory.horizontal_separator_params_large()
        #params_section = GenUtils.ParamsSectionFactory.beppy()
        print(params_section)
        params_windows = GenMesh.ParamsWindows.from_ui()
        params_cage = NewMesh.ParamsWindowCage.from_ui()

        sequence = GenUtils.gen_simple_section_list(params_windows.section_width, params_windows.section_height)
        m_section = GenUtils.gen_section_mesh(sequence, params_windows.frame_width,
                                              params_windows.frame_depth)
        bm_section = bmesh.new()
        bm_section.from_mesh(m_section)
        '''
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        mat_rot = mathutils.Matrix.Rotation(math.radians(-90), 3, "X")
        vec_trans = (0.0, -params_windows.frame_width, 0.0)
        bmesh.ops.rotate(bm_section, cent=(0, 0, 0), matrix=mat_rot, verts=bm_section.verts, space=mat_loc)
        bmesh.ops.translate(bm_section, vec=vec_trans, space=mat_loc, verts=bm_section.verts)
        bm_section.to_mesh(m_section)
        '''

        my_window = GenMesh.gen_mesh_windows(context, params_general, params_windows)
        group.objects.link(my_window)
        my_window_around = GenMesh.gen_mesh_windows_around(context, params_general, params_windows)
        my_bar = NewMesh.gen_mesh_window_cage(context, params_cage, params_general)

        # just using these window params as arbitrary values.
        awning_profile_list = GenUtils.gen_awning_section_list(25, 3, 1, 0.03)
        awning_profile = GenUtils.gen_plane_profile( awning_profile_list, params_windows.frame_width )

        awning_section = bmesh.new()
        awning_section.from_mesh(awning_profile)

        m = bpy.data.meshes.new("test")
        awning_section.to_mesh(m)
        awning_section.free()

        test_obj = bpy.data.objects.new( "test", m )
        context.scene.collection.objects.link(test_obj)     
 
     awning = NewMesh.gen_window_awning( context, params_general )
            apply_positions( awning, layout["window_positions"], group )
   
        '''
        m = bpy.data.meshes.new("WindowCageBar")
        my_bar.to_mesh(m)
        my_bar.free()
        ob = bpy.data.objects.get("WindowCageBar")
        if ob is not None:
            #context.scene.objects.unlink(ob)
            bpy.data.objects.remove(ob)

        # link the created object to the scene
        new_obj = bpy.data.objects.new("WindowCageBar", m)
        context.scene.collection.objects.link(new_obj)
        '''

        #group.objects.link(my_window)
        origin = (0,0,0)
        #apply_positions(my_window, origin, group)
        return {"FINISHED"}
    # end invoke
# end MyGenerator
"""


