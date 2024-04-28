#Author: NSA Cloud
import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
					   CollectionProperty,
                       )
import os
def update_relPathToAbs(self,context):
	try:
		if "//" in self.path:
			#print("updated path")
			self.path = os.path.realpath(bpy.path.abspath(self.path))
	except:
		pass
	
def update_EditorTabVis(self, context):
	if self.hideREChainEditor:
		context.scene["HIDE_RE_CHAIN_EDITOR_TAB"] = 1
	else:
		if "HIDE_RE_CHAIN_EDITOR_TAB" in context.scene:
			del context.scene["HIDE_RE_CHAIN_EDITOR_TAB"]
	
	if self.hideREMeshEditor:
		context.scene["HIDE_RE_MDF_EDITOR_TAB"] = 1
	else:
		if "HIDE_RE_MDF_EDITOR_TAB" in context.scene:
			del context.scene["HIDE_RE_MDF_EDITOR_TAB"]
			
	if self.hideREMapEditor:
		context.scene["HIDE_RE_MAP_EDITOR_TAB"] = 1
	else:
		if "HIDE_RE_MAP_EDITOR_TAB" in context.scene:
			del context.scene["HIDE_RE_MAP_EDITOR_TAB"]
	
	if self.hideREMotionEditor:
		context.scene["HIDE_RE_MOTION_EDITOR_TAB"] = 1
	else:
		if "HIDE_RE_MOTION_EDITOR_TAB" in context.scene:
			del context.scene["HIDE_RE_MOTION_EDITOR_TAB"]
		
			
		
class ExportEntryPropertyGroup(bpy.types.PropertyGroup):
	enabled: BoolProperty(
		name="",
		description = "Export this file",
		default = True
	)
	fileType: EnumProperty(
		name="",
		description="Set the type of file to be exported",
		items= [ 
        ("MESH", "MESH", ""),
		("MDF", "MDF", ""),
		("CHAIN", "CHAIN", ""),
		("FBXSKEL", "FBXSKEL", ""),
		("MCOL", "MCOL", ""),
		("SCN", "SCN", ""),
		("USER", "USER", ""),
		("PFB", "PFB", ""),
		("MOT", "MOT", ""),
		("MOTLIST", "MOTLIST", ""),
		]
    )
	path: StringProperty(
        name="",
		subtype="FILE_PATH",
		description = "Path to where to export the file to",
		update = update_relPathToAbs
	)

	#mesh operator arguments
	meshCollection: bpy.props.StringProperty(
		name="",
		description = "Set the collection containing the meshes to be exported",
		
		)
	
	exportAllLODs : BoolProperty(
	   name = "Export All LODs",
	   description = "Export all LODs. If disabled, only LOD0 will be exported. Note that LODs meshes must be grouped inside a collection for each level and that collection must be contained in another collection. See a mesh with LODs imported for reference on how it should look. A target collection must also be set",
	   default = False)
	exportBlendShapes : BoolProperty(
	   name = "Export Blend Shapes",
	   description = "Exports blend shapes from mesh if present",
	   default = True)
	autoSolveRepeatedUVs : BoolProperty(
	   name = "Auto Solve Repeated UVs",
	   description = "Splits connected UV islands if present. The mesh format does not allow for multiple uvs assigned to a vertex.\nNOTE: This will modify the object and may slightly increase time taken to export",
	   default = True)
	preserveSharpEdges : BoolProperty(
	   name = "Add Edge Split Modifier",
	   description = "Adds an edge split modifier set to sharp edges for all objects. This prevents edges that are marked as sharp from being lost",
	   default = True)
	rotate90 : BoolProperty(
	   name = "Convert Z Up To Y Up",
	   description = "Rotates objects 90 degrees for export. Leaving this option enabled is recommended",
	   default = True)
	useBlenderMaterialName : BoolProperty(
	   name = "Use Blender Material Names",
	   description = "If left unchecked, the exporter will get the material names to be used from the end of each object name. For example, if a mesh is named LOD_0_Group_0_Sub_0__Shirts_Mat, the material name is Shirts_Mat. If this option is enabled, the material name will instead be taken from the first material assigned to the object",
	   default = False)
	preserveBoneMatrices : BoolProperty(
	   name = "Preserve Bone Matrices",
	   description = "Export using the original matrices of the imported bones. Note that this option only applies armatures imported with this addon. Any newly added bones will have new matrices calculated",
	   default = False)
	exportBoundingBoxes : BoolProperty(
	   name = "Export Bounding Boxes",
	   description = "Exports the original bounding boxes from the \"Import Bounding Boxes\" import option. New bounding boxes will be generated for any bones that do not have them",
	   default = False)
	#mdf operator arguments
	mdfCollection: bpy.props.StringProperty(
		name="",
		description = "Set the MDF collection to be exported",
		)
	#chain operator arguments
	chainCollection: bpy.props.StringProperty(
		name="",
		description = "Set the chain collection to be exported",
		)
	rootObject: bpy.props.StringProperty(
		name="",
		description = "Set the RSZ root object",
		)
class MESH_UL_BatchExportList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		layout.prop(item,"enabled")
		#row = layout.row()
		#row.alignment = "LEFT"
		#row.prop(item,"fileType")
		layout.prop(item,"path",text = item.fileType)
		#row.operator("re_toolbox.set_batch_export_options",text = "",icon = "PREFERENCES")
class REToolboxPanelPropertyGroup(bpy.types.PropertyGroup):
    
	hideREMeshEditor : BoolProperty(
	   name = "Hide RE MDF Tab",
	   description = "Hides the RE MDF tab on the sidebar",
	   default = False,
	   update = update_EditorTabVis)
	
	hideREChainEditor : BoolProperty(
	   name = "Hide RE Chain Tab",
	   description = "Hides the RE Chain tab on the sidebar",
	   default = False,
	   update = update_EditorTabVis)
	
	hideREMapEditor : BoolProperty(
	   name = "Hide RE Map Tools Tab",
	   description = "Hides the RE Map Tools tab on the sidebar",
	   default = False,
	   update = update_EditorTabVis)
	
	hideREMotionEditor : BoolProperty(
	   name = "Hide RE Motion Tab",
	   description = "Hides the RE Motion tab on the sidebar",
	   default = False,
	   update = update_EditorTabVis)
	
	batchExportList_items: CollectionProperty(type=ExportEntryPropertyGroup)
	batchExportList_index: IntProperty(name="")