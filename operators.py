# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty
from bpy_extras.io_utils import ImportHelper
import csv, shutil, zipfile, os, glob, fnmatch

class ISN_OT_import_zip(Operator, ImportHelper):
    """Imports Syncsketch's notes (Maya greasepencil zip) as camera background sequence."""
    bl_idname = 'isn.import_zip'
    bl_label = 'Import Syncsketch Notes'
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = '.zip'
    
    filter_glob: StringProperty(
        default='*.zip',
        options={'HIDDEN'}
    )

    def execute(self, context):
        zipFile = self.filepath
        zipName = os.path.basename(zipFile).split('/')[-1]
        zipPath = os.path.dirname(os.path.abspath(zipFile))
        blendPath = bpy.path.abspath("//")
        notesTarget = blendPath + 'SyncsketchNotes\\' + os.path.splitext(zipName)[0]
        
        print(f'imported file (full): {zipFile}')
        print(f'imported file name: {zipName}')
        print(f'imported file path: {zipPath}')
        print(f'blend path: {blendPath}')
        print(f'target notes path: {notesTarget}')
        
        
        with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
            zip_ref.extractall(notesTarget)


        for file in os.listdir(notesTarget):
            if fnmatch.fnmatch(file, '*.png'):
                noteFile = file
                notePath = notesTarget + '\\' + noteFile
                print(f'    Notes Files: {noteFile}')
                break
            else: 
                self.report({'WARNING'}, f'No sketches found in {notesTarget}')
                return {'FINISHED'}
            
        cam = bpy.context.scene.camera
        
        for bgi in cam.data.background_images:
            if bgi.image and bgi.image.name == 'SyncsketchNotes':
                bpy.data.images.remove(bpy.data.images["SyncsketchNotes"])
                cam.data.background_images.remove(bgi)
                cam.data.background_images.update()
                break

        img = bpy.data.images.load(notePath)
        img.source = 'SEQUENCE'
        img.name = 'SyncsketchNotes'
        cam.data.show_background_images = True
        bg = cam.data.background_images.new()
        bg.image = img
        bg.image_user.frame_duration = bpy.context.scene.frame_end
        bg.image_user.frame_start = 1
        bg.frame_method = 'CROP'
        
        cam.data.background_images.update()
        
        return {'FINISHED'}

class ISN_OT_jumpToFrame(Operator):
    """Tooltip"""
    bl_idname = "isn.jump_to_frame"
    bl_label = "Jump to frame"
    bl_options = {'REGISTER', "UNDO"}
    
    frameJump: IntProperty()

    def execute(self, context):
        bpy.context.scene.frame_set(self.frameJump)
        return {'FINISHED'}

class ISN_OT_import_csv(Operator, ImportHelper):
    """Imports Syncsketch's notes (Maya greasepencil zip) as camera background sequence."""
    bl_idname = 'isn.import_csv'
    bl_label = 'Import Syncsketch Comments'
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = '.csv'
    
    filter_glob: StringProperty(
        default='*.csv',
        options={'HIDDEN'}
    )

    def execute(self, context):
        csvFile = self.filepath
        csvName = os.path.basename(csvFile).split('/')[-1]
        csvPath = os.path.dirname(os.path.abspath(csvFile))
        blendPath = bpy.path.abspath("//")
        commentsTarget = blendPath + 'SyncsketchNotes\\' + os.path.splitext(csvName)[0]

        print(f'imported file (full): {csvFile}')
        print(f'imported file name: {csvName}')
        print(f'imported file path: {csvPath}')
        print(f'blend path: {blendPath}')
        print(f'target notes path: {commentsTarget}')

        shutil.copy2(csvFile, commentsTarget)

        for txt in bpy.data.texts:
            if txt.name == 'SyncsketchComments':
                bpy.data.texts.remove(bpy.data.texts["SyncsketchComments"])

        txt = bpy.data.texts.load(csvFile)
        txt.name = 'SyncsketchComments'


        return {'FINISHED'}

class ISN_OT_delete_notes(Operator):
    bl_idname = 'isn.delete_notes'
    bl_label = 'Deletes Syncsketch Notes'
    bl_options = {'PRESET', 'UNDO'}

    def execute(self, context):
        cam = bpy.context.scene.camera
        for bgi in cam.data.background_images:
            if bgi.image and bgi.image.name == 'SyncsketchNotes':
                bpy.data.images.remove(bpy.data.images["SyncsketchNotes"])
                cam.data.background_images.remove(bgi)
                cam.data.background_images.update()
                break
        return {'FINISHED'}

class ISN_OT_delete_comments(Operator):
    bl_idname = 'isn.delete_comments'
    bl_label = 'Deletes Syncsketch Comments'
    bl_options = {'PRESET', 'UNDO'}
    
    def execute(self, context):
        for txt in bpy.data.texts:
            if txt.name == 'SyncsketchComments':
                bpy.data.texts.remove(bpy.data.texts["SyncsketchComments"])
                break
        return {'FINISHED'}

classes = (
    ISN_OT_import_zip,
    ISN_OT_jumpToFrame,
    ISN_OT_import_csv,
    ISN_OT_delete_notes,
    ISN_OT_delete_comments,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    try:
        import os
        os.remove(os.path.join(os.path.expanduser("~"), "temp.txt"))
    except:
        pass