# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty

from .bl_class_registry import BlClassRegistry
from .panels import (
    ISN_PT_mainPanel,
    ISN_PT_commentsPanel,
    )


@BlClassRegistry()
class ISNPreferences(AddonPreferences):
    bl_idname = __package__

    def _panel_category_update(self, context):

        panels = [
            ISN_PT_mainPanel,
            ISN_PT_commentsPanel,
        ]

        for panel in panels:
            has_panel = hasattr(bpy.types, panel.bl_idname)
            if has_panel:
                try:
                    bpy.utils.unregister_class(panel)
                except:
                    pass
            panel.bl_category = self.panel_category
            bpy.utils.register_class(panel)

    panel_category: StringProperty(
        name="Panel Category",
        description="Category to show \"Import Syncsketch Notes\" panel",
        default="Animation",
        update=_panel_category_update,
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Set the category to show Bone-Widgets panel:")
        col.prop(self, "panel_category")
