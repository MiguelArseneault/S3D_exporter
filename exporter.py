import bpy
from bpy_extras.io_utils import ExportHelper
import os

bl_info = {
	"name": "Export Stupid3D (.s3d)",
	"author": "Super-Go-Team-Squad",
	"version": (1, 1),
	"blender": (2, 5, 7),
	"api": 35622,
	"location": "File > Export",
	"description": "Exports Model to Stupid3D File Format",
	"warning": "",
	"wiki_url": "https://github.com/MiguelArseneault/S3D_exporter/wiki",
	"tracker_url": "https://github.com/MiguelArseneault/S3D_exporter/issues",
	"support": "COMMUNITY",
	"category": "Import-Export"}

### EXPORT OPERATOR ###
class Export_s3d(bpy.types.Operator, ExportHelper):
	bl_description = "Exports the active Object as a Stupid3D file."
	bl_idname = "export_object.s3d"
	bl_label = "Export Stupid3D (.s3d)"
	extension = ".s3d"

	def do_export(context, props, filepath):
		with open(filepath, "w+") as file:
			Export_s3d.SaveData(file, bpy.context.object.data)

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
			file.write("\n" if (index+1 % 12 == 0) else " ")
			
		# Free the normals
		mesh.free_normals_split()

	def execute(self, context):
		filepath = bpy.path.ensure_ext(self.filepath, self.extension)
		exported = Export_s3d.do_export(context, self.properties, filepath)
		print("Saved file to:", filepath)
		return {'FINISHED'}

	def invoke(self, context, event):
		# File selector
		context.window_manager.fileselect_add(self) # will run self.execute()
		return {'RUNNING_MODAL'}

### REGISTER ###
def menu_func(self, context):
	self.layout.operator(Export_s3d.bl_idname, text="Stupid3D (.s3d)")

def register():
	bpy.utils.register_module(__name__)

	bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)

	bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
	register()