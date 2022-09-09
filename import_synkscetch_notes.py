import bpy
import zipfile, os, glob, fnmatch
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class

# C:\Users\Roikku\Documents\Taff\Perso\Animation\Shorts\Emotional Scars Never Heal!\greasepencil\08_splining_074_0001-0118.greasepencil.zip
### Import Syncsketch Notes  - ISN

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
        
        bpy.context.scene.camera.data.background_images.clear()

        img = bpy.data.images.load(notePath)
        img.source = 'SEQUENCE'
        img.name = 'SyncsketchNotes'
        cam.data.show_background_images = True
        bg = cam.data.background_images.new()
        bg.image = img
        bg.image_user.frame_duration = bpy.context.scene.frame_end
        bg.image_user.frame_start = 1
        bg.frame_method = 'CROP'
        
            
#        print(next(glob.iglob(join(notesTarget, ".png"))))
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ISN_OT_import_zip.bl_idname, text="Syncsketch Notes", icon='GREASEPENCIL')

def register():
    bpy.utils.register_class(ISN_OT_import_zip)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ISN_OT_import_zip)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
#    bpy.ops.isn.import_zip('INVOKE_DEFAULT')