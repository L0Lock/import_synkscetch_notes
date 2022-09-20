# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu
from .operators import (
    ISN_OT_import_zip,
    ISN_OT_import_csv,
)

class ISN_MT_syncsketch_import(Menu):
    bl_label = "Syncsketch"
    bl_idname = 'isn.import_menu'

    def draw(self, context):
        layout = self.layout
        layout.operator(ISN_OT_import_zip.bl_idname, text="Notes", icon='GREASEPENCIL')
        layout.operator(ISN_OT_import_csv.bl_idname, text="Comments", icon='FILE_TEXT')

def draw_menu(self, context):
    self.layout.menu(ISN_MT_syncsketch_import.bl_idname)


classes = (
    ISN_MT_syncsketch_import,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(draw_menu)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(draw_menu)
