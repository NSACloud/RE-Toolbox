import bpy
import os
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


def tag_redraw(context, space_type="PROPERTIES", region_type="WINDOW"):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.spaces[0].type == space_type:
                for region in area.regions:
                    if region.type == region_type:
                        region.tag_redraw()


class OBJECT_PT_REToolsMeshToolsPanel(Panel):
	bl_label = "RE Toolbox: Mesh Tools"
	bl_idname = "OBJECT_PT_re_tools_mesh_tools_panel"
	bl_space_type = "VIEW_3D"   
	bl_region_type = "UI"
	bl_category = "RE Toolbox"

	@classmethod
	def poll(self,context):
		return context is not None

	def draw(self, context):
		layout = self.layout
		layout.operator("re_toolbox.create_mesh_collection")
		layout.operator("re_toolbox.solve_repeated_uvs")
		layout.operator("re_toolbox.split_sharp_edges")
		layout.operator("re_toolbox.rename_meshes")
		layout.operator("re_toolbox.triangulate_meshes")
		layout.operator("re_toolbox.delete_loose")
		layout.operator("re_toolbox.remove_zero_weight_vertex_groups")
		layout.operator("re_toolbox.limit_total_normalize")

class OBJECT_PT_REToolsVisibilityPanel(Panel):
	bl_label = "RE Toolbox: Tab Visibility"
	bl_idname = "OBJECT_PT_re_tools_visibility_panel"
	bl_space_type = "VIEW_3D"   
	bl_region_type = "UI"
	bl_category = "RE Toolbox"

	@classmethod
	def poll(self,context):
		return context is not None

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		re_toolbox_toolpanel = scene.re_toolbox_toolpanel
		layout.prop(re_toolbox_toolpanel,"hideREMeshEditor")
		layout.prop(re_toolbox_toolpanel,"hideREChainEditor")
		#layout.prop(re_toolbox_toolpanel,"hideREMapEditor")
		#layout.prop(re_toolbox_toolpanel,"hideREMotionEditor")
        
class OBJECT_PT_REToolsQuickExportPanel(Panel):
	bl_label = "RE Toolbox: Batch Export"
	bl_idname = "OBJECT_PT_re_tools_quick_export_panel"
	bl_space_type = "VIEW_3D"   
	bl_region_type = "UI"
	bl_category = "RE Toolbox"

	@classmethod
	def poll(self,context):
		return context is not None

	def draw(self, context):
		scene = context.scene
		re_toolbox_toolpanel = scene.re_toolbox_toolpanel
		layout = self.layout
		layout.label(text = "Batch Export List")
		row = layout.row()
		row.template_list("MESH_UL_BatchExportList", "", re_toolbox_toolpanel, "batchExportList_items", re_toolbox_toolpanel, "batchExportList_index",rows = 4)
		col = row.column(align=True)
		col.operator("re_toolbox.batch_export_list_add_item",text="",icon = "ADD")
		col.operator("re_toolbox.batch_export_list_remove_item",text="",icon = "REMOVE")
		col.separator()
		col.operator("re_toolbox.batch_export_list_reorder_item", text="",icon = "TRIA_UP").direction = 'UP'
		col.operator("re_toolbox.batch_export_list_reorder_item", text="",icon = "TRIA_DOWN").direction = 'DOWN'
		itemIndex = context.scene.re_toolbox_toolpanel.batchExportList_index
		if len(context.scene.re_toolbox_toolpanel.batchExportList_items) != 0 and itemIndex < len(context.scene.re_toolbox_toolpanel.batchExportList_items):
			exportItem = context.scene.re_toolbox_toolpanel.batchExportList_items[context.scene.re_toolbox_toolpanel.batchExportList_index]
			fileName = os.path.splitext(os.path.split(exportItem.path)[1])[0]
		else:
			fileName = ""
		layout.label(text = f"Selected Item: {fileName}")
		
		layout.operator("re_toolbox.set_batch_export_options",text = "Set Export Options")
		layout.operator("re_toolbox.quick_export")