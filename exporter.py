import bpy, bmesh, os
from bpy_extras.io_utils import ExportHelper

bl_info = {
	"name": "Export Stupid3D (.s3d)",
	"author": "Super-Go-Team-Squad",
	"version": (1, 2),
	"blender": (2, 5, 7),
	"api": 35622,
	"location": "File > Export",
	"description": "Exports Model to Stupid3D File Format",
	"warning": "",
	"wiki_url": "https://github.com/MiguelArseneault/S3D_exporter/wiki",
	"tracker_url": "https://github.com/MiguelArseneault/S3D_exporter/issues",
	"support": "COMMUNITY",
	"category": "Import-Export"}

class MockUV:
	pass

### EXPORT OPERATOR ###
class Export_s3d(bpy.types.Operator, ExportHelper):
	bl_description = "Exports the active Object as a Stupid3D file."
	bl_idname = "export_object.s3d"
	bl_label = "Export Stupid3D (.s3d)"
	filename_ext = ".s3d"

	def do_export(context, props, filepath):
		with open(filepath, "w+") as file:
			Export_s3d.SaveData(file, bpy.context.object.data)

	#Miguel's_Stuff #GetitTrending
	def triangulate_mesh(mesh):
		# Get a BMesh representation
		bm = bmesh.new()
		bm.from_mesh(mesh)

		bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)

		# Finish up, write the bmesh back to the mesh
		new_mesh = bpy.data.meshes.new("temp")
		bm.to_mesh(new_mesh)
		bm.free()
		return new_mesh

	def Deduplicate(vertices, indices):
		# Sets duplicate vertices to Null and points indices to sole vertice of that kind
		for index, vertice in enumerate(vertices[:-2]):
			for index2, vertice2 in enumerate(vertices[index+1:]):
				if vertice == vertice2:
					indices[index+index2+1] = index
					vertices[index+index2+1] = None
		
		# Offset indices from the top
		for index, vertice in list(enumerate(vertices))[::-1]:
			if vertice == None:
				for index2, indexValue in enumerate(indices):
					if indexValue > index:
						indices[index2] -= 1
		# Crunch None vertices
		vertices = [vertice for vertice in vertices if vertice != None ]

		# Return deduplicated vertices and indices
		return vertices, indices

	def SaveData(file, mesh):
		# Triangulate the mesh
		mesh = Export_s3d.triangulate_mesh(mesh)

		# Calculate normals
		mesh.calc_normals_split()
		
		# Get the first UV layer (if it exists)
		uv_layer = None
		if (len(mesh.uv_layers) > 0):
			uv_layer = mesh.uv_layers[0]
		
		# Get the vertex data
		vertices = []
		for index, loop in enumerate(mesh.loops):
			# Get all vertice data (coordinates, normals, and UVs)
			vertice = mesh.vertices[loop.vertex_index]
			uv_loop = None
			if uv_layer != None:
				uv_loop = uv_layer.data[index]
			else:
				uv_loop = MockUV()
				uv_loop.uv = (0.0, 0.0)
			
			# Store vertices in a list of tuples
			vertices.append((vertice.co[0], vertice.co[1], vertice.co[2],
							 loop.normal[0], loop.normal[1], loop.normal[2],
							 uv_loop.uv[0], uv_loop.uv[1],))
		
		# Get a list of all the indices
		indices = list(range(len(vertices)))

		# Deduplicate the vertices and indices
		vertices, indices = Export_s3d.Deduplicate(vertices, indices)

		# Write the number of vertices
		file.write(str(len(vertices))+"\n")

		# Write vertice data
		for vertice in vertices:
			# Generate line to write to file
			line = ""
			for number in vertice:
				line += str(number)+" "
			line = line[:-1]+"\n"

			# Write line to file
			file.write(line)

		# Write the number of indices
		file.write(str(len(indices))+"\n")
		
		# Write indice data
		for index, vindex in enumerate(indices):
			file.write(str(vindex))
			file.write("\n" if ((index+1) % 3 == 0) else " ")
			
		# Free the normals
		mesh.free_normals_split()

	def execute(self, context):
		filepath = bpy.path.ensure_ext(self.filepath, self.filename_ext)
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