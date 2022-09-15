import bpy
from bpy.types import Panel, Operator
from bpy.props import IntProperty
from rna_prop_ui import PropertyPanel
from bl_ui.utils import PresetPanel
import csv
import textwrap

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

    def _getCsvList(self):
        
#        csvFile = open("C:\\Users\\Roikku\\Documents\\Repositories\\import_synkscetch_notes\\Workbench\\test.csv", "r")
        # outfile = open("C:\\Users\\Roikku\\Documents\\Repositories\\import_synkscetch_notes\\Workbench\\SynckSketchComments.md", "w")
        quote_character='"'
        delimiter=','

        with open("C:\\Users\\Roikku\\Documents\\Repositories\\import_synkscetch_notes\\Workbench\\test.csv", "r") as csvFile:
            reader = csv.DictReader(csvFile, delimiter=delimiter, quotechar=quote_character, restkey='unrecognized_cols')
            csvList = list()
            for dictionary in reader:
                csvList.append(dictionary)
        return(csvList)

    def _dpi_scale(self):
        return bpy.context.preferences.system.pixel_size
    
    def _region_width(self):
        return bpy.context.region.width
    
    def _char_width(self):
        rawWidth = self._region_width()
        width = (rawWidth*0.9)/6
        
        # apply scale factor for retina screens etc
        width = int(width / self._dpi_scale())
        # padding to account for some kerning
#        self.wrap = width/7
        
        return width
    
    def _wrapper(self, textTowrap ):
        wrapp = textwrap.TextWrapper(self._char_width(),)
        wrapList = wrapp.wrap(text=textTowrap) 
        
        return wrapList

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = context.camera
        width = self._char_width()

        csvList = self._getCsvList()

        ReviewName = csvList[1]["Review Name"]
        ItemName = csvList[1]["Item Name"]
        ItemLink = csvList[1]["Link"].split("#")[0]
        # csvFile.readline()
        # last_pos = csvFile.tell()
        # split_line = csvFile.readline().split(",")
        # ReviewName = split_line[1]
        # ItemName = split_line[3]
        # split_link = split_line[11].split("#")
        # ItemLink = split_link[0]

        row=layout.row()
        box=layout.box()
        box.scale_y = 1
        box.label(text=f'Review: {ReviewName}')
        row=box.row()
        row.label(text=f'File: {ItemName}')
        row.operator("wm.url_open", text="", icon='LINK_BLEND').url = ItemLink

        row=layout.row()
        
        # csvFile.seek(last_pos)
        # Loop line by line extracting variables for the fields
        # Export the file as a markdown file.
        for line in csvList:
            NoteFrame = line["Frame Number"]
            Author = line["Full Name"]
            Comment = self._wrapper(line["Comment"])
            Date = line["Date Created"].split(' ')[0]
            box=layout.box()
            box.scale_y = 1
            row=box.row()
            row.label(text=f'Frame: {NoteFrame.rjust(4)}')
            props = row.operator("isn.jump_to_frame", text="", icon='NEXT_KEYFRAME')
            props.frameJump = int(NoteFrame)
            row=box.row()
            row.label(text=f'{Author}')
            row.label(text=f'noted on {Date}')
            row.alignment = 'LEFT'
            box.label(text='·'*int(width*1.64))
            for text in Comment: 
#                box.(align = True)
                box.alignment = 'EXPAND'
                box.label(text=text)
#            box.label(text=f'{Comment}')
            # print(f'| {NoteFrame} | *{Author}*:<br/>{Comment} |',file=outfile)
        # csvFile.close()
        # outfile.close()
        
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
