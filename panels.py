# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Panel
from bpy.props import BoolProperty
from .functions import (
    _char_width,
    _getCsvList,
    _wrapper,
)
from .operators import (
    ISN_OT_import_csv,
    ISN_OT_import_zip,
    ISN_OT_delete_notes,
    ISN_OT_delete_comments,
)
from .bl_class_registry import BlClassRegistry
# from .menus import BONEWIDGET_MT_bw_specials


@BlClassRegistry()

class ISN_PT_mainPanel(Panel):
    bl_label = 'Syncsketch Feedback'
    bl_idname = 'VIEW3D_PT_isn_main_panel'
    bl_category = "Animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text='Import:')
        row.operator(ISN_OT_import_zip.bl_idname, text="Notes", icon='GREASEPENCIL')
        row.operator(ISN_OT_import_csv.bl_idname, text="Comments", icon='FILE_TEXT')

        # bpy.data.images["SyncsketchNotes"].name

        cam = bpy.context.scene.camera
        
        for bgi in cam.data.background_images:
            if bgi.image and bgi.image.name == 'SyncsketchNotes':
                layout = self.layout
                row = layout.row(align=True)
                row.prop(
                    bgi,
                    "show_background_image",
                    text='Display Notes',
                    icon='RESTRICT_VIEW_OFF' if bgi.show_background_image else 'RESTRICT_VIEW_ON',
                    )
                row.operator('isn.delete_notes', text='', icon='X')
                break


class ISN_PT_commentsPanel(Panel):
    bl_label = 'Comments'
    bl_idname = 'VIEW3D_PT_isn_comments_panel'
    bl_category = "Animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_isn_main_panel"

    def draw(self, context):
        layout = self.layout

        width = _char_width()
        csvList = _getCsvList()

        if csvList == None:
            row=layout.row()
            box=layout.box()
            box.scale_y = 1
            box.label(text=f'No comments to display')
        else:
            layout.operator('isn.delete_comments', text='Remove Notes', icon='X')

            ReviewName = csvList[1]["Review Name"]
            ItemName = csvList[1]["Item Name"]
            ItemLink = csvList[1]["Link"].split("#")[0]

            row=layout.row()
            box=layout.box()
            box.scale_y = 1
            box.label(text=f'Review: {ReviewName}')
            row=box.row()
            row.label(text=f'File: {ItemName}')
            row.operator("wm.url_open", text="", icon='LINK_BLEND').url = ItemLink

            row=layout.row()
            
            for line in csvList:
                NoteFrame = line["Frame Number"]
                Author = line["Full Name"]
                Comment = _wrapper(line["Comment"])
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
                    box.alignment = 'EXPAND'
                    box.label(text=text)
