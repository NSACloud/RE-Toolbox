#Author: NSA Cloud
bl_info = {
    "name": "RE Toolbox",
    "author": "NSA Cloud",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Tool Shelf > RE Toolbox",
    "description": "Extra utilities to make working with RE Engine files easier",
    "warning": "",
    "wiki_url": "https://github.com/NSACloud/RE-Toolbox",
    "tracker_url": "https://github.com/NSACloud/RE-Toolbox/issues",
    "category": "3D View"}

import bpy
from . import addon_updater_ops
import os

from bpy.types import AddonPreferences
from .modules.re_toolbox_propertyGroups import ExportEntryPropertyGroup,MESH_UL_BatchExportList,REToolboxPanelPropertyGroup
from .modules.ui_re_toolbox_panels import OBJECT_PT_REToolsMeshToolsPanel,OBJECT_PT_REToolsVisibilityPanel,OBJECT_PT_REToolsQuickExportPanel
from .modules.re_toolbox_operators import (WM_OT_AddItemOperator,
										WM_OT_RemoveItemOperator,
										WM_OT_ReorderItemOperator,
										WM_OT_AddBoneNumbers,
                                        WM_OT_RemoveBoneNumbers,
                                        WM_OT_SeparateChainBones,
                                        WM_OT_TriangulateMeshes,
                                        WM_OT_SolveRepeatedUVs,
                                        WM_OT_DeleteLoose,
										WM_OT_RenameMeshToREFormat,
                                        #WM_OT_RenameMHWToMHR,
                                        #WM_OT_RenameMHRToMHW,
                                        WM_OT_RemoveZeroWeightVertexGroups,
                                        #WM_OT_TransferWeightsFromActive,
                                        WM_OT_LimitTotalNormalizeAll,
                                        WM_OT_QuickExport,
										WM_OT_SetBatchExportOptions,
                                        
                                        )
class REToolboxPreferences(AddonPreferences):
	bl_idname = __name__
	# addon updater preferences
	auto_check_update: bpy.props.BoolProperty(
	    name = "Auto-check for Update",
	    description = "If enabled, auto-check for updates using an interval",
	    default = False,
	)
	
	updater_interval_months: bpy.props.IntProperty(
	    name='Months',
	    description = "Number of months between checking for updates",
	    default=0,
	    min=0
	)
	updater_interval_days: bpy.props.IntProperty(
	    name='Days',
	    description = "Number of days between checking for updates",
	    default=7,
	    min=0,
	)
	updater_interval_hours: bpy.props.IntProperty(
	    name='Hours',
	    description = "Number of hours between checking for updates",
	    default=0,
	    min=0,
	    max=23
	)
	updater_interval_minutes: bpy.props.IntProperty(
	    name='Minutes',
	    description = "Number of minutes between checking for updates",
	    default=0,
	    min=0,
	    max=59
	)
	def draw(self, context):
		layout = self.layout
		split = layout.split(factor = .3)
		col1 = split.column()
		col2 = split.column()
		col3 = split.column()
		op = col2.operator(
        'wm.url_open',
        text='Donate on Ko-fi',
        icon='FUND'
        )
		op.url = 'https://ko-fi.com/nsacloud'
		addon_updater_ops.update_settings_ui(self,context)
os.system("color")#Enable console colors

# Registration
classes = [
	REToolboxPreferences,
	ExportEntryPropertyGroup,
	MESH_UL_BatchExportList,
    REToolboxPanelPropertyGroup,
    OBJECT_PT_REToolsMeshToolsPanel,
	OBJECT_PT_REToolsVisibilityPanel,
    OBJECT_PT_REToolsQuickExportPanel,
	WM_OT_AddItemOperator,
	WM_OT_RemoveItemOperator,
	WM_OT_ReorderItemOperator,
	WM_OT_SetBatchExportOptions,
    WM_OT_AddBoneNumbers,
    WM_OT_RemoveBoneNumbers,
    WM_OT_SeparateChainBones,
    WM_OT_TriangulateMeshes,
    WM_OT_SolveRepeatedUVs,
    WM_OT_DeleteLoose,
	WM_OT_RenameMeshToREFormat,
    #WM_OT_RenameMHWToMHR,
    #WM_OT_RenameMHRToMHW,
    WM_OT_RemoveZeroWeightVertexGroups,
    #WM_OT_TransferWeightsFromActive,
    WM_OT_LimitTotalNormalizeAll,
    WM_OT_QuickExport
    ]


def register():
	
	addon_updater_ops.register(bl_info)
	for classEntry in classes:
		bpy.utils.register_class(classEntry)
        
	bpy.types.Scene.re_toolbox_toolpanel = bpy.props.PointerProperty(type=REToolboxPanelPropertyGroup)
def unregister():
	addon_updater_ops.unregister()
	for classEntry in classes:
		bpy.utils.unregister_class(classEntry)
        
if __name__ == '__main__':
    register()