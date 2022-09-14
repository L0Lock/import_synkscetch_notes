import bpy
from bpy.types import Panel, Operator
from bpy.props import IntProperty
from rna_prop_ui import PropertyPanel
from bl_ui.utils import PresetPanel
import csv

class CameraButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        engine = context.engine
        return context.camera and (engine in cls.COMPAT_ENGINES)
    
class ISN_OT_jumpToFrame(Operator):
    """Tooltip"""
    bl_idname = "isn.jump_to_frame"
    bl_label = "Jump to frame"
    bl_options = {'REGISTER', "UNDO"}
    
    frameJump: IntProperty()

    def execute(self, context):
        bpy.context.scene.frame_set(self.frameJump)
        return {'FINISHED'}

class ISN_PT_syncsketch(CameraButtonsPanel, Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Syncsketch Comments"

    @classmethod
    def poll(cls, context):
        engine = context.engine
        return context.camera

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = context.camera
        
        infile = open("C:\\Users\\Roikku\\Documents\\Repositories\\import_synkscetch_notes\\Workbench\\12575762_08_Splining_074_0001-0118_2022-09-14-020950262677.csv", "r")
        outfile = open("C:\\Users\\Roikku\\Documents\\Repositories\\import_synkscetch_notes\\Workbench\\SynckSketchComments.md", "w")
        infile.readline()
        last_pos = infile.tell()
        split_line = infile.readline().split(",")
        ReviewName = split_line[1]
        ItemName = split_line[3]
        split_link = split_line[11].split("#")
        ItemLink = split_link[0]

        row=layout.row()
        box=layout.box()
        box.scale_y = 1
        box.label(text=f'Review: {ReviewName}')
        row=box.row()
        row.label(text=f'File: {ItemName}')
        row.operator("wm.url_open", text="", icon='LINK_BLEND').url = ItemLink

        row=layout.row()
        
        infile.seek(last_pos)
        # Loop line by line extracting variables for the fields
        # Export the file as a markdown file.
        for line in infile.readlines():
            split_line = line.split(",")
            NoteFrame = split_line[6]
            Author = split_line[10]
            Comment = split_line[8]
            box=layout.box()
            box.scale_y = 1
            row=box.row()
            row.label(text=f'Frame: {NoteFrame.rjust(4)}')
            props = row.operator("isn.jump_to_frame", text="", icon='NEXT_KEYFRAME')
            props.frameJump = int(NoteFrame)
            row=box.row()
            box.label(text=f'{Author} noted: {Comment}')
            
            
#            print(f'| {NoteFrame} | *{Author}*:<br/>{Comment} |',file=outfile)
        infile.close()
        outfile.close()
        
classes = (
    ISN_OT_jumpToFrame,
    ISN_PT_syncsketch,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.frameJump = IntProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.frameJump


if __name__ == "__main__":  # only for live edit.
    register()
#    unregister()
