bl_info = {
    "name": "Camera Selector",
    "author": "Teitetsu",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "location": "View3D > Sidebar > View > Camera Selector",
    "description": "Camera Select Tools",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Camera",
}

import bpy


########################################
# Operator
########################################
 
class CameraPicker(bpy.types.Operator):
    bl_idname      = "camera_selector.camera_picker"
    bl_label       = "Camera Picker"
    bl_description = "Set Picked Camera To Active"
    
    def invoke(self, context, event):       
        
        the_camera = context.the_camera
        selected_cam = sorted([o for o in bpy.context.selected_objects if o.type == 'CAMERA'],key=lambda o: o.name)
        
        if event.shift:
            if the_camera in selected_cam:
                # Deselect
                the_camera.select_set(state = False)
            else:
                # Sellect Add
                the_camera.select_set(state = True)
                bpy.context.view_layer.objects.active = the_camera
        else:
            # Deselect all
            if bpy.context.mode == 'OBJECT':
                bpy.ops.object.select_all(action='DESELECT')
            
            # Select Camera
            the_camera.select_set(state = True)
            bpy.context.view_layer.objects.active = the_camera
        return {'FINISHED'}


class SetSceneCamera(bpy.types.Operator):    
    bl_idname      = "camera_selector.set_scene_camera"
    bl_label       = "Set Scene Camera"
    bl_description = "Set Active Camera To Scene Camera"
    
    def invoke(self, context, event):
        
        # Set Secnecamera
        the_camera = context.the_camera
        bpy.context.scene.camera = the_camera
        
        
        # Set Camera Resolution to Secne Resoluton
        x = the_camera.data.get("resolution_x",0)
        y = the_camera.data.get("resolution_y",0)         
        if type(x) == int and x > 0 and type(y) == int and y > 0:
            render = bpy.context.scene.render
            render.resolution_x = x
            render.resolution_y = y
        
        # Set Current Frame
        current_frame = the_camera.data.get("current_freme")
        if type(current_frame) == int:
            bpy.context.scene.frame_current = current_frame
        
        return {'FINISHED'}


class SaveCustomResolution(bpy.types.Operator):
    bl_idname      = "camera_selector.save_custom_resolution"
    bl_label       = "Save Custom Resolution"
    bl_description = "Save Render Resolution to Camera Custom Property"
    
    def execute(self, context):
        the_camera = bpy.context.scene.camera
        render = bpy.context.scene.render
        
        x = render.resolution_x
        y = render.resolution_y
        
        if (the_camera):
            the_camera.data["resolution_x"] = x
            the_camera.data["resolution_y"] = y
        return {'FINISHED'}


class SaveCustomFrame(bpy.types.Operator):
    bl_idname      = "camera_selector.save_custom_flame"
    bl_label       = "Save Custom Frame"
    bl_description = "Save Current Frame to Camera Custom Property"
    
    def execute(self, context):
        the_camera = bpy.context.scene.camera
        current_frame = bpy.context.scene.frame_current
        
        if (the_camera) and (current_frame):
            the_camera.data["current_freme"] = current_frame
        return {'FINISHED'}
    
    

########################################
# Panel
########################################

class CameraSelectorMenu(bpy.types.Panel):
    bl_idname       = "CAMERASELECTOR_PT_Menu"
    bl_label        = "Camera Selector"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "View"
    
    def draw(self, context):
        layout = self.layout
        scene   = context.scene
        cameras = sorted([i for i in scene.objects if i.type == 'CAMERA'],key=lambda i: i.name)
        SceneCam = bpy.context.scene.camera
        
        row = layout.row()
        row.alignment = 'RIGHT'
        row.label(text="Filter:")
        row.prop(scene,"visible_filter",icon = 'HIDE_OFF',icon_only = True,toggle = -1)
        
        for camera in cameras:
            if not(scene.visible_filter == True and camera.visible_get() == False):                
                row    = layout.row(align = True)
                row.context_pointer_set("the_camera", camera)
                row.operator("camera_selector.camera_picker",text = "",icon='RESTRICT_SELECT_OFF') 
                row.operator("camera_selector.set_scene_camera",text = camera.name,icon='CAMERA_DATA') 
        
        layout.separator()
        if (SceneCam):
            box = layout.box()
            box.label(text = "Scene Camera")
            box.prop(SceneCam.data,"lens")
            box.prop(SceneCam.data,"shift_x")
            box.prop(SceneCam.data,"shift_y")
            box.prop(SceneCam.data,"passepartout_alpha")
            box.separator()
            box.label(text = "Save")
            row = box.row(align = True)
            row.operator("camera_selector.save_custom_resolution",text = "Resoluton",icon='IMAGE_BACKGROUND')
            row.operator("camera_selector.save_custom_flame",text = "Frame",icon='PLAY')
        


########################################
# Regester
########################################

def register():
    # Custom Rroperty
    bpy.types.Scene.visible_filter = bpy.props.BoolProperty(name="Visible Filter")
    # Operators
    bpy.utils.register_class(CameraPicker)
    bpy.utils.register_class(SetSceneCamera)
    bpy.utils.register_class(SaveCustomResolution)
    bpy.utils.register_class(SaveCustomFrame)
    # Panel
    bpy.utils.register_class(CameraSelectorMenu)


def unregister():
    # Operators
    bpy.utils.unregister_class(CameraPicker)
    bpy.utils.unregister_class(SetSceneCamera)
    bpy.utils.unregister_class(SaveCustomResolution)
    bpy.utils.unregister_class(SaveCustomFrame)
    # Panel
    bpy.utils.unregister_class(CameraSelectorMenu)
    # Custom Rroperty
    if hasattr(bpy.types.Scene, "visible_filter"):
        del bpy.types.Scene.visible_filter


if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
