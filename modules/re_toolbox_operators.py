#Author: NSA Cloud
import bpy
import os
import bmesh
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from .blender_utils import showMessageBox,showErrorMessageBox
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       )

fileExtensionToEnumDict = {
	".mesh":"MESH",
	".mdf2":"MDF",
	".chain":"CHAIN",
	".fbxskel":"FBXSKEL",
	".mcol":"MCOL",
	".scn":"SCN",
	".user":"USER",
	".pfb":"PFB",
	".mot":"MOT",
	".motlist":"MOTLIST",
	
	
	}
class WM_OT_AddItemOperator(bpy.types.Operator,ImportHelper):
	bl_idname = "re_toolbox.batch_export_list_add_item"
	bl_description = "Add a file to export to the batch export list"
	bl_label = "Add Path"
	def invoke(self,context,event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
    
	def execute(self, context):
		# Add an item to the list
		if "//" in self.filepath:
			#print("updated path")
			self.filepath = os.path.realpath(bpy.path.abspath(self.filepath))
		
		#print(self.filepath)
		try:
			fileExtension = os.path.splitext(os.path.splitext(os.path.split(self.filepath)[1])[0])[1]
			#print(fileExtension)
			if fileExtension not in fileExtensionToEnumDict:
				raise
		except:
			showErrorMessageBox("Invalid file type.")
			return {'CANCELLED'}
		if os.path.isfile(self.filepath):
			exportItem = context.scene.re_toolbox_toolpanel.batchExportList_items.add()
			exportItem.fileType = fileExtensionToEnumDict[fileExtension]
			exportItem.path = self.filepath
			context.scene.re_toolbox_toolpanel.batchExportList_index = len(context.scene.re_toolbox_toolpanel.batchExportList_items) - 1
		else:
			showErrorMessageBox("Invalid file path.")
			return {'CANCELLED'}
		return {'FINISHED'}
# Operator to remove an item from the list
class WM_OT_RemoveItemOperator(bpy.types.Operator):
	bl_idname = "re_toolbox.batch_export_list_remove_item"
	bl_description = "Remove an item from the batch export list"
	bl_label = "Remove Selected Path"

	index: bpy.props.IntProperty()

	def execute(self, context):
        # Remove the item at the specified index from the list
		context.scene.re_toolbox_toolpanel.batchExportList_items.remove(self.index)
		return {'FINISHED'}

# Operator to reorder items in the list
class WM_OT_ReorderItemOperator(bpy.types.Operator):
	bl_idname = "re_toolbox.batch_export_list_reorder_item"
	bl_label = "Reorder Item"
	bl_description = "Move an item in the list up or down to change the order of export"
	direction: bpy.props.EnumProperty(
		items=[('UP', "Up", ""), ('DOWN', "Down", "")],
		default='UP'
	)

	index: bpy.props.IntProperty()

	def execute(self, context):
		# Reorder the item in the list
		if self.direction == 'UP':
			context.scene.re_toolbox_toolpanel.batchExportList_items.move(self.index, self.index - 1)
		elif self.direction == 'DOWN':
			context.scene.re_toolbox_toolpanel.batchExportList_items.move(self.index, self.index + 1)
		return {'FINISHED'}

#Armature Operators

class WM_OT_AddBoneNumbers(Operator):
	"""Add bone numbers to armatures"""
	bl_label = "Add Bone Numbers"
	bl_idname = "re_toolbox.add_bone_numbers"

	def execute(self, context):
		#If bone is in use by meshes, give it a bone number
		
		for obj in bpy.context.selected_objects:
			if obj.type == "ARMATURE":
				index = 1
				vgSet = set()
				for child in obj.children:
					if child.type == "MESH":
						vgSet.update(set(child.vertex_groups.keys()))
				for bone in obj.data.bones:
					if bone.name in vgSet:
						if not ":" in bone.name:
							bone.name = "b"+str(index).zfill(3)+":"+bone.name
							index += 1
		self.report({"INFO"},"Added bone numbers to armatures.")
		return {'FINISHED'}
class WM_OT_RemoveBoneNumbers(Operator):
	"""Remove bone numbers from armatures"""
	bl_label = "Remove Bone Numbers"
	bl_idname = "re_toolbox.remove_bone_numbers"

	def execute(self, context):
		for armature in bpy.data.armatures:
			for bone in armature.bones:
				if ":" in bone.name:
					bone.name = bone.name.split(":")[1]
		self.report({"INFO"},"Removed bone numbers from armatures.")
		return {'FINISHED'}

class WM_OT_SeparateChainBones(Operator):
	"""Separate chain bones from armature into their own armature. NOTE: RE Chain Editor must be installed and a chain file must be imported"""
	bl_label = "Separate Chain Bones"
	bl_idname = "re_toolbox.separate_chain_bones"
	
	@classmethod
	def poll(self,context):
		return "RE-Chain-Editor" in bpy.context.preferences.addons.keys()
	
	def execute(self, context):
		currentMode = bpy.context.object.mode
		#Find all chain groups
		for chainGroupObj in [obj for obj in bpy.context.scene.objects if obj.get("TYPE",None) =="RE_CHAIN_CHAINGROUP"]:
			if chainGroupObj.children != []:
				#Get node hierarchy from chain group
				currentNode = chainGroupObj.children[0]
				nodeObjList = [currentNode]
				while len(currentNode.children) > 1:
					for child in currentNode.children:
						if child["TYPE"] == "RE_CHAIN_NODE":
							nodeObjList.append(child)
							
							currentNode = child
				#print(nodeObjList)
				#Find child of constraint to get armature
				currentGroupArmature = None
				for constraint in nodeObjList[0].constraints:
					if (constraint.type == "CHILD_OF" and constraint.name == "BoneName"):
						if constraint.target != None:
							if constraint.target.type == "ARMATURE":
								currentGroupArmature = constraint.target
				if currentGroupArmature != None:
					armatureCopy = currentGroupArmature.copy()
					armatureCopy.data = armatureCopy.data.copy()#Make armature object unique
					armatureCopy.name = "Armature_"+chainGroupObj.name
					bpy.context.collection.objects.link(armatureCopy)
					#or bone in currentGroupArmature.data.bones:
						#if bone in nodeObjList
				#print(nodeObjList[0].modifiers)
				#if nodeObjList[0].modifiers.get("BoneName",None)
				nodeObjList.reverse()
				#TODO Create copy of armature, remove all bones other than one's nodes are parented to
				
				#TODO Change child of constraint on nodes to new armature
				bpy.context.view_layer.update()
				
		return {'FINISHED'}


#Mesh Operators

class WM_OT_TriangulateMeshes(Operator):
	"""Triangulate all meshes in scene"""
	bl_label = "Triangulate Meshes"
	bl_idname = "re_toolbox.triangulate_meshes"
	bl_description = "Triangute selected meshes"
	def execute(self, context):
		for selectedObj in context.selected_objects:
			if selectedObj.type == "MESH":
				context.view_layer.objects.active  = selectedObj
				bpy.ops.object.mode_set(mode='EDIT')
				bpy.ops.mesh.select_all(action='SELECT')
				print(f"Triangulated faces on {selectedObj.name}")
				bpy.ops.mesh.quads_convert_to_tris()
				bpy.ops.object.mode_set(mode='OBJECT')
		self.report({"INFO"},"Triangulated faces on selected objects")


		return {'FINISHED'}

class WM_OT_SolveRepeatedUVs(Operator):
	bl_label = "Solve Repeated UVs"
	bl_idname = "re_toolbox.solve_repeated_uvs"
	bl_description = "Splits connected UV islands"
	def execute(self, context):
		for selectedObj in context.selected_objects:
			if selectedObj.type == "MESH":
				context.view_layer.objects.active  = selectedObj
				bpy.ops.object.mode_set(mode='EDIT')
				obj = context.edit_object
				me = obj.data
				bm = bmesh.from_edit_mesh(me)
				# old seams
				old_seams = [e for e in bm.edges if e.seam]
				# unmark
				for e in old_seams:
				    e.seam = False
				# mark seams from uv islands
				bpy.ops.mesh.select_all(action='SELECT')
				bpy.ops.uv.select_all(action='SELECT')
				bpy.ops.uv.seams_from_islands()
				seams = [e for e in bm.edges if e.seam]
				bmesh.ops.split_edges(bm, edges=seams)
				for e in old_seams:
				    e.seam = True
				bmesh.update_edit_mesh(me)
				bpy.ops.object.mode_set(mode='OBJECT')
				print(f"Solved Repeated UVs on {selectedObj.name}")
		return {'FINISHED'}
	
	
class WM_OT_DeleteLoose(Operator):
	bl_label = "Delete Loose Geometry"
	bl_idname = "re_toolbox.delete_loose"
	bl_description = "Deletes loose vertices and edges with no faces on selected meshes"
	def execute(self, context):
		for selectedObj in context.selected_objects:
			if selectedObj.type == "MESH":
				context.view_layer.objects.active  = selectedObj
				bpy.ops.object.mode_set(mode='EDIT')
				bpy.ops.mesh.select_all(action='SELECT')
				print(f"Deleted loose geometry on {selectedObj.name}")
				bpy.ops.mesh.delete_loose()
				bpy.ops.object.mode_set(mode='OBJECT')
		self.report({"INFO"},"Deleted loose geometry on selected objects")
		return {'FINISHED'}
class WM_OT_RenameMeshToREFormat(Operator):
	bl_label = "Rename Meshes"
	bl_idname = "re_toolbox.rename_meshes"
	bl_description = "Renames selected meshes to RE mesh naming scheme (Example: Group_0_Sub_0__Shirts_Mat)"
	def execute(self, context):
		currentSubIndex = 0
		for selectedObj in context.selected_objects:
			if selectedObj.type == "MESH":
				if len(selectedObj.data.materials) > 0:
					materialName = selectedObj.data.materials[0].name.split(".",1)[0].strip()
				else:
					materialName = "NO_MATERIAL"
				selectedObj.name = f"Group_0_Sub_{str(currentSubIndex)}__{materialName}"
				currentSubIndex += 1
		self.report({"INFO"},"Renamed selected objects to RE Mesh format")
		return {'FINISHED'}
#Weights
class WM_OT_RenameMHWToMHR(Operator):
	"""Rename vertex groups from their Monster Hunter World bones to the equivalent Monster Hunter Rise bones"""
	bl_label = "Rename MHW Bones to MHR"
	bl_idname = "re_toolbox.mhw_to_mhr"

	def execute(self, context):
		for obj in bpy.data.objects:
			v_groups = obj.vertex_groups
			name_list = [
		    # old name - new name
		
		
		
		    ['Waist_00', 'BoneFunction.013'],
		    ['Spine_00', 'BoneFunction.001'],
		    ['Spine_01', 'BoneFunction.002'],
		    ['Neck_00', 'BoneFunction.003'],
		    ['Head_00', 'BoneFunction.004'],
		    ['L_Arm_00', 'BoneFunction.005'],
		    ['L_Arm_01', 'BoneFunction.006'],
		    ['L_Arm_02', 'BoneFunction.007'],
		    ['L_Arm_03', 'BoneFunction.008'],
		    ['L_Finger_00', 'BoneFunction.031'],
		    ['L_Finger_01', 'BoneFunction.032'],
		    ['L_Finger_02', 'BoneFunction.033'],
		    ['L_Finger_03', 'BoneFunction.034'],
		    ['L_Finger_04', 'BoneFunction.035'],
		    ['L_Finger_05', 'BoneFunction.036'],
		    ['L_Finger_06', 'BoneFunction.037'],
		    ['L_Finger_07', 'BoneFunction.038'],
		    ['L_Finger_08', 'BoneFunction.039'],
		    ['L_Finger_09', 'BoneFunction.040'],
		    ['L_Finger_10', 'BoneFunction.041'],
		    ['L_Finger_11', 'BoneFunction.042'],
		    ['L_Finger_12', 'BoneFunction.043'],
		    ['L_Finger_13', 'BoneFunction.044'],
		    ['L_Finger_14', 'BoneFunction.045'],
		    ['L_Finger_15', 'BoneFunction.046'],
		    ['L_Arm_00_W', 'BoneFunction.070'],
		    ['L_Arm_01_W', 'BoneFunction.071'],
		    ['L_Arm_01_T', 'BoneFunction.080'],
		    ['R_Arm_00', 'BoneFunction.009'],
		    ['R_Arm_01', 'BoneFunction.010'],
		    ['R_Arm_02', 'BoneFunction.011'],
		    ['R_Arm_03', 'BoneFunction.012'],
		    ['R_Finger_00', 'BoneFunction.048'],
		    ['R_Finger_01', 'BoneFunction.049'],
		    ['R_Finger_02', 'BoneFunction.050'],
		    ['R_Finger_03', 'BoneFunction.051'],
		    ['R_Finger_04', 'BoneFunction.052'],
		    ['R_Finger_05', 'BoneFunction.053'],
		    ['R_Finger_06', 'BoneFunction.054'],
		    ['R_Finger_07', 'BoneFunction.055'],
		    ['R_Finger_08', 'BoneFunction.056'],
		    ['R_Grip_00', 'BoneFunction.057'],
		    ['R_Finger_09', 'BoneFunction.058'],
		    ['R_Finger_10', 'BoneFunction.059'],
		    ['R_Finger_11', 'BoneFunction.060'],
		    ['R_Finger_12', 'BoneFunction.061'],
		    ['R_Finger_13', 'BoneFunction.062'],
		    ['R_Finger_14', 'BoneFunction.063'],
		    ['R_Arm_00_W', 'BoneFunction.072'],
		    ['R_Arm_01_W', 'BoneFunction.073'],
		    ['R_Arm_01_T', 'BoneFunction.082'],
		    
		    ['R_Leg_00', 'BoneFunction.018'],
		    ['R_Leg_01', 'BoneFunction.019'],
		    ['R_Leg_02', 'BoneFunction.020'],
		    ['R_Leg_03', 'BoneFunction.021'],
		    ['R_Leg_01_W', 'BoneFunction.077'],
		    ['R_Leg_00_W', 'BoneFunction.076'],
		    
		    ['L_Leg_00', 'BoneFunction.014'],
		    ['L_Leg_01', 'BoneFunction.015'],
		    ['L_Leg_02', 'BoneFunction.016'],
		    ['L_Leg_03', 'BoneFunction.017'],
		    ['L_Leg_01_W', 'BoneFunction.075'],
		    ['L_Leg_00_W', 'BoneFunction.074']]
			
			for n in name_list:
				if n[1] in v_groups:
					v_groups[n[1]].name = n[0]
		
		return {'FINISHED'}
	
class WM_OT_RenameMHRToMHW(Operator):
	"""Rename vertex groups from their Monster Hunter Rise bones to the equivalent Monster Hunter World bones"""
	bl_label = "Rename MHR Bones to MHW"
	bl_idname = "re_toolbox.mhr_to_mhw"

	def execute(self, context):
		
		return {'FINISHED'}

class WM_OT_RemoveZeroWeightVertexGroups(Operator):
	"""Remove all vertex groups that have no weight assigned to them"""
	bl_label = "Remove Empty Vertex Groups"
	bl_idname = "re_toolbox.remove_zero_weight_vertex_groups"

	def execute(self, context):
		for obj in bpy.context.selected_objects:
			emptyGroupList = []
			for vertexGroup in obj.vertex_groups:
				if not any(vertexGroup.index in [g.group for g in v.groups] for v in obj.data.vertices):
					emptyGroupList.append(vertexGroup)
			for group in emptyGroupList:
				obj.vertex_groups.remove(group)
		return {'FINISHED'}
	
class WM_OT_TransferWeightsFromActive(Operator):
	"""Transfer weights from the active object to all other selected objects. NOTE: This does not do all the work of weighting, you should still manually fix up the resulting weights"""
	bl_label = "Transfer Weights From Active Object"
	bl_idname = "re_toolbox.transfer_weights_from_active"

	def execute(self, context):
		showMessageBox(message = "Not implemented yet.", title = "Not Implemented")#TODO

		return {'FINISHED'}
	
class WM_OT_LimitTotalNormalizeAll(Operator):
	"""Limits the amount of bones influences per vertex to 8 and normalizes the weights of all vertex groups for all selected meshes"""
	bl_label = "Limit Total and Normalize All"
	bl_idname = "re_toolbox.limit_total_normalize"

	def execute(self, context):
		for selectedObj in context.selected_objects:
			if selectedObj.type == "MESH":
				context.view_layer.objects.active  = selectedObj
				bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
				bpy.ops.object.vertex_group_limit_total(limit = 8)
				bpy.ops.object.vertex_group_normalize_all(lock_active = False)
				print(f"Limited total weights to 8 and normalized {selectedObj.name}")
				bpy.ops.object.mode_set(mode='OBJECT')
				self.report({"INFO"},"Limited total weights and normalized on selected objects")
		return {'FINISHED'}
#Quick Export
class WM_OT_SetBatchExportOptions(Operator):
	bl_label = "Export Options"
	bl_description = "Set the export options of the batch export entry"
	bl_idname = "re_toolbox.set_batch_export_options"
	bl_context = "objectmode"
	
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
	rotate90 : BoolProperty(
	   name = "Convert Z Up To Y Up",
	   description = "Rotates objects 90 degrees for export. Leaving this option enabled is recommended",
	   default = True)
	autoSolveRepeatedUVs : BoolProperty(
	   name = "Auto Solve Repeated UVs",
	   description = "(RE Toolbox Required)\nSplits connected UV islands if present. The mesh format does not allow for multiple uvs assigned to a vertex.\nNOTE: This will modify the object and may slightly increase time taken to export",
	   default = True)
	preserveSharpEdges : BoolProperty(
	   name = "Add Edge Split Modifier",
	   description = "Adds an edge split modifier set to sharp edges for all objects. This prevents edges that are marked as sharp from being lost",
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
	@classmethod
	def poll(self,context):
		return context is not None
	def draw(self, context):
		layout = self.layout
		itemIndex = context.scene.re_toolbox_toolpanel.batchExportList_index
		if itemIndex != -1:
			exportItem = context.scene.re_toolbox_toolpanel.batchExportList_items[context.scene.re_toolbox_toolpanel.batchExportList_index]
			fileName = os.path.splitext(os.path.split(exportItem.path)[1])[0]
			layout.label(text = f"List Item {str(itemIndex + 1)}: {fileName}")
			if exportItem.fileType == "MESH":
				layout.label(text = "Target Collection:")
				layout.prop_search(self, "meshCollection",bpy.data,"collections",icon = "COLLECTION_COLOR_01")
				layout.label(text = "Advanced Options")
				layout.prop(self, "exportAllLODs")
				#layout.prop(self, "exportBlendShapes")
				layout.prop(self,"autoSolveRepeatedUVs")
				layout.prop(self,"preserveSharpEdges")
				layout.prop(self, "rotate90")
				layout.prop(self, "useBlenderMaterialName")
				layout.prop(self, "preserveBoneMatrices")
				layout.prop(self, "exportBoundingBoxes")
			elif exportItem.fileType == "MDF":
				layout.label(text = "MDF Collection:")
				layout.prop_search(self, "mdfCollection",bpy.data,"collections",icon = "COLLECTION_COLOR_05")
				
			elif exportItem.fileType == "CHAIN":
				layout.label(text = "Chain Collection:")
				layout.prop_search(self, "chainCollection",bpy.data,"collections",icon = "COLLECTION_COLOR_02")
			else:
				layout.label(text = "No export options available.")
	def execute(self, context):
		if len(context.scene.re_toolbox_toolpanel.batchExportList_items) != 0:	
			exportItem = context.scene.re_toolbox_toolpanel.batchExportList_items[context.scene.re_toolbox_toolpanel.batchExportList_index]
			exportItem.meshCollection = self.meshCollection
			exportItem.exportAllLODs = self.exportAllLODs
			exportItem.rotate90 = self.rotate90
			exportItem.autoSolveRepeatedUVs = self.autoSolveRepeatedUVs
			exportItem.preserveSharpEdges = self.preserveSharpEdges
			exportItem.useBlenderMaterialName = self.useBlenderMaterialName
			exportItem.preserveBoneMatrices = self.preserveBoneMatrices
			exportItem.exportBoundingBoxes = self.exportBoundingBoxes
			exportItem.mdfCollection = self.mdfCollection
			exportItem.chainCollection = self.chainCollection
			self.report({"INFO"},f"Set export options of list item {str(context.scene.re_toolbox_toolpanel.batchExportList_index)}")
		return {'FINISHED'}
	def invoke(self,context,event):
		exportItem = None
		if len(context.scene.re_toolbox_toolpanel.batchExportList_items) != 0:
			exportItem = context.scene.re_toolbox_toolpanel.batchExportList_items[context.scene.re_toolbox_toolpanel.batchExportList_index]
		if exportItem != None:
			self.meshCollection = exportItem.meshCollection
			self.exportAllLODs = exportItem.exportAllLODs
			self.autoSolveRepeatedUVs = exportItem.autoSolveRepeatedUVs
			self.preserveSharpEdges = exportItem.preserveSharpEdges
			self.rotate90 = exportItem.rotate90
			self.useBlenderMaterialName = exportItem.useBlenderMaterialName
			self.preserveBoneMatrices = exportItem.preserveBoneMatrices
			self.exportBoundingBoxes = exportItem.exportBoundingBoxes
			self.mdfCollection = exportItem.mdfCollection
			self.chainCollection = exportItem.chainCollection
			return context.window_manager.invoke_props_dialog(self)
		else:
			showErrorMessageBox("No items in batch export list.")
			return {"FINISHED"}
class WM_OT_QuickExport(Operator):
	bl_label = "Batch Export"
	bl_idname = "re_toolbox.quick_export"

	def execute(self, context):
		showMessageBox(message = "Not implemented yet.", title = "Not Implemented")#TODO

		return {'FINISHED'}
class WM_OT_QuickExport(Operator):
	bl_label = "Batch Export"
	bl_idname = "re_toolbox.quick_export"

	def execute(self, context):
		print("Batch export started.")
		for exportItem in context.scene.re_toolbox_toolpanel.batchExportList_items:
			if exportItem.enabled:
				if exportItem.fileType == "MESH":
					if hasattr(bpy.types, "OBJECT_PT_mdf_tools_panel"): 
						try:
							bpy.ops.re_mesh.exportfile(
								filepath = exportItem.path,
								targetCollection = exportItem.meshCollection,
								exportAllLODs = exportItem.exportAllLODs,
								autoSolveRepeatedUVs = exportItem.autoSolveRepeatedUVs,
								preserveSharpEdges = exportItem.preserveSharpEdges,
								rotate90 = exportItem.rotate90,
								useBlenderMaterialName = exportItem.useBlenderMaterialName,
								preserveBoneMatrices = exportItem.preserveBoneMatrices,
								exportBoundingBoxes = exportItem.exportBoundingBoxes,
								)
						except Exception as err:
							print(f"Mesh Export Failed: {str(err)}")
					else:
						print("RE Mesh Editor is not installed. Skipping batch export entry.")
				
				elif exportItem.fileType == "MDF":
					if hasattr(bpy.types, "OBJECT_PT_mdf_tools_panel"):
						try:
							bpy.ops.re_mdf.exportfile(
								filepath = exportItem.path,
								targetCollection = exportItem.mdfCollection,
								)
						except Exception as err:
							print(f"MDF Export Failed: {str(err)}")
					else:
						print("RE Mesh Editor is not installed. Skipping batch export entry.")
				elif exportItem.fileType == "CHAIN":
					if hasattr(bpy.types, "OBJECT_PT_chain_object_mode_panel"):
						try:
							bpy.ops.re_chain.exportfile(
								filepath = exportItem.path,
								targetCollection = exportItem.chainCollection,
								)
						except Exception as err:
							print(f"Chain Export Failed: {str(err)}")
					else:
						print("RE Chain Editor is not installed. Skipping batch export entry.")
				elif exportItem.fileType == "SCN" or exportItem.fileType == "PFB" or exportItem.fileType == "USER":
					if hasattr(bpy.types, "OBJECT_PT_re_map_tools_object_panel"):
						try:
							bpy.ops.re_scene.exportfile(
								filepath = exportItem.path,
								rootObject = exportItem.rootObject,
								)
						except Exception as err:
							print(f"RSZ Export Failed: {str(err)}")
					else:
						print("RE Map Editor is not installed. Skipping batch export entry.")
				elif exportItem.fileType == "MCOL":
					if hasattr(bpy.types, "OBJECT_PT_re_map_tools_object_panel"):
						try:
							bpy.ops.re_mcol.exportfile(
								filepath = exportItem.path,
								collisionMesh = exportItem.rootObject,
								)
						except Exception as err:
							print(f"MCOL Export Failed: {str(err)}")
					else:
						print("RE Map Editor is not installed. Skipping batch export entry.")
				else:
					print(f"Unsupported File Type ({exportItem.fileType}), skipping")
		self.report({"INFO"},"Batch export finished.")
		return {'FINISHED'}