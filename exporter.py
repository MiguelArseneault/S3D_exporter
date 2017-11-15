bl_info = {
	"name": "Export Stupid3D (.s3d)",
	"author": "Super-Go-Team-Squad",
	"version": (1, 0),
	"blender": (2, 5, 7),
	"api": 35622,
	"location": "File > Export",
	"description": "Export Model to Stupid3D",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"}

'''
Usage Notes:
'''

import bpy
from bpy.props import *
import mathutils, math, struct
import os
from os import remove
import time
import bpy_extras
from bpy_extras.io_utils import ExportHelper 
import time
import shutil
import bpy
import mathutils

def writeString(file, string):
	file.write(bytes(string, 'UTF-8'))

def do_export(context, props, filepath):

	file = open(filepath, "w+")
	mesh = bpy.context.object.data
	SaveData(file, mesh)
	file.close()

	#Miguel's_Stuff #GetitTrending
def SaveData(file, mesh):
    # Calculate normals
    mesh.calc_normals_split()
    
    # Get the first UV layer
    uv_layer = None
    if (len(mesh.uv_layers) > 0):
        uv_layer = mesh.uv_layers[0]
    
    # Declaring some variables yo
    vertice = None
    uv_loop = None
    line = ""
    
    # Write the number of vertices
    file.write(str(len(mesh.loops))+"\n")
    
    # Write the vertex data
    for index,loop in enumerate(mesh.loops):
        line = ""
        vertice = mesh.vertices[loop.vertex_index]
        uv_loop = uv_layer.data[index]
        line += str(vertice.co[0])+" "
        line += str(vertice.co[1])+" "
        line += str(vertice.co[2])+" "
        line += str(loop.normal[0])+" "
        line += str(loop.normal[1])+" "
        line += str(loop.normal[2])+" "
        line += str(uv_loop.uv[0])+" "
        line += str(uv_loop.uv[1])+"\n"
        file.write(line)
        
    # Write the number of indices
    file.write(str(len(mesh.loops))+"\n")
    
    # Write indice data
    for index in range(len(mesh.loops)):
        file.write(str(index))
        file.write("\n" if (index % 12 == 0) else " ")
        
    # Free the normals
    mesh.free_normals_split()

###### EXPORT OPERATOR #######
class Export_objc(bpy.types.Operator, ExportHelper):
	'''Exports the active Object as a Stupid3D file.'''
	bl_idname = "export_object.objc"
	bl_label = "Export Stupid3D (.s3d)"

	filename_ext = ".s3d"
	
	apply_modifiers = BoolProperty(name="Apply Modifiers",
							description="Applies the Modifiers",
							default=True)

	rot_x90 = BoolProperty(name="Convert to Y-up",
							description="Rotate 90 degrees around X to convert to y-up",
							default=True)
	
	world_space = BoolProperty(name="Export into Worldspace",
							description="Transform the Vertexcoordinates into Worldspace",
							default=False)

	
	@classmethod
	def poll(cls, context):
		return context.active_object.type in ['MESH', 'CURVE', 'SURFACE', 'FONT']

	def execute(self, context):
		start_time = time.time()
		print('\n_____START_____')
		props = self.properties
		filepath = self.filepath
		filepath = bpy.path.ensure_ext(filepath, self.filename_ext)

		exported = do_export(context, props, filepath)
		
		if exported:
			print('finished export in %s seconds' %((time.time() - start_time)))
			print(filepath)
			
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager

		if True:
			# File selector
			wm.fileselect_add(self) # will run self.execute()
			return {'RUNNING_MODAL'}
		elif True:
			# search the enum
			wm.invoke_search_popup(self)
			return {'RUNNING_MODAL'}
		elif False:
			# Redo popup
			return wm.invoke_props_popup(self, event) #
		elif False:
			return self.execute(context)


### REGISTER ###

def menu_func(self, context):
	self.layout.operator(Export_objc.bl_idname, text="Stupid3D (.s3d)")

def register():
	bpy.utils.register_module(__name__)

	bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)

	bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
	register()