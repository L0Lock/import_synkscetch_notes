# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Import Syncsketch Notes - Pack",
    "author": "Loïc Dautry (L0Lock)",
    "version": (0, 0, 3),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Animation tab > Syncsketch Notes",
    "description": "Imports Syncsketch's notes and comments."
                   "On Syncsketch, you need to download notes from \"Maya greasepencil File...\" and comments from the CSV file.",
    "warning": "In development!",
    "doc_url": "https://github.com/L0Lock/import_synkscetch_notes",
    "wiki_url": "",
    "tracker_url": "https://github.com/L0Lock/import_synkscetch_notes/issues",
    "support": 'COMMUNITY',
    "category": "Import-Export",
}

if "bpy" in locals():
    import importlib
    bl_class_registry.BlClassRegistry.cleanup()
    importlib.reload(prefs)
    importlib.reload(panels)
    importlib.reload(menus)

else:
    import bpy
    from . import bl_class_registry
    from . import operators
    from . import panels
    from . import prefs
    from . import menus

import bpy
import os

def get_user_preferences(context):
    if hasattr(context, "user_preferences"):
        return context.user_preferences

    return context.preferences

def check_version(major, minor, _):
    """
    Check blender version
    """

    if bpy.app.version[0] == major and bpy.app.version[1] == minor:
        return 0
    if bpy.app.version[0] > major:
        return 1
    if bpy.app.version[1] > minor:
        return 1
    return -1

def register():
    operators.register()
    menus.register()
    bl_class_registry.BlClassRegistry.register()

    # Apply preferences of the panel location.
    context = bpy.context
    pref = get_user_preferences(context).addons[__package__].preferences
    # Only default panel location is available in < 2.80
    if check_version(2, 80, 0) < 0:
        pref.panel_category = "Rig Tools"
    prefs.ISNPreferences._panel_category_update(pref, context)


def unregister():
    operators.unregister()
    menus.unregister()
    # TODO: Unregister by BlClassRegistry
    bl_class_registry.BlClassRegistry.unregister()


if __name__ == "__main__":
    register()
