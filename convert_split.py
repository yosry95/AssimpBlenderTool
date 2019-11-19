import os
import argparse
import bpy
import time
import shutil
import mmap
import re

def get_args():
  parser = argparse.ArgumentParser()
 
  # get all script args
  _, all_arguments = parser.parse_known_args()
  double_dash_index = all_arguments.index('--')
  script_args = all_arguments[double_dash_index + 1: ]
 
  # add parser rules
  parser.add_argument('-i', '--Inobj', help="In OBJ file")
  parser.add_argument('-o', '--Outfbx', help="Out FBX file")
  parser.add_argument('-f', '--Infbx', help="In FBX file")
  
  parsed_script_args, _ = parser.parse_known_args(script_args)
  return parsed_script_args

# get the arguments
args = get_args()

# arguments summary
print("*******************************************************")
print("**")
print("** IN-File: " + str(args.Inobj))
print("** OUT-File: " + str(args.Outfbx))
print("** IN-File: " + str(args.Infbx))
print("**")
print("*******************************************************")

flag = False
fileName = args.Inobj[:-3]+"mtl"
print("*******************************************************")
print("**")
print("** Searching for .fbm in the .mtl file")
print("**")
print("*******************************************************")
with open(fileName, 'rb', 0) as file, \
     mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
		if re.search(br'(?i).fbm', s):
			flag = True
			print("*******************************************************")
			print("**")
			print("** found fbm in the file")
			print("**")
			print("*******************************************************")
			bpy.ops.wm.read_homefile(use_empty=True)
			print("*******************************************************")
			print("**")
			print("** Opening FBX File")
			print("**")
			print("*******************************************************")
			bpy.ops.import_scene.fbx(filepath=args.Infbx)
			if os.path.isdir(os.getcwd()+'\\textures'):
				shutil.rmtree(os.getcwd()+'\\textures')			
			bpy.ops.file.unpack_all(method = 'WRITE_LOCAL')

			if os.path.isdir(os.getcwd()+'\\textures'):
				srcPath = os.getcwd() + '\\' + str(args.Infbx)[11:-3] +"fbm"
				desPath = os.getcwd() + '\\outputFiles\\' + str(args.Infbx)[11:-3] +"fbm"

				for filename in os.listdir(os.getcwd()+'\\textures'):
					infilename = os.path.join(os.getcwd()+'\\textures', filename)
					if not os.path.isfile(infilename): continue
					oldbase = os.path.splitext(filename)
					newname =  infilename.replace('.fbm', '.png')
					output = os.rename(infilename, newname)
					
				os.rename('textures',str(args.Infbx)[11:-3] +"fbm")
				print(srcPath)
				
				
				## Check if old .fbm file in destination is available
				if os.path.isdir(desPath):
					shutil.rmtree(desPath)
				shutil.move(srcPath,desPath)
				
				print("*******************************************************")
				print("**")
				print("** End Exporting the .fbm file")
				print("**")
				print("*******************************************************")
print("*******************************************************")
print("**")
print("** End Searching for .fbm in the .mtl file")
print("**")
print("*******************************************************")

# Open empty scene
bpy.ops.wm.read_homefile(use_empty=True)
# import scene
bpy.ops.import_scene.obj(filepath=args.Inobj, use_split_objects=False, use_split_groups=False) 
#bpy.ops.import_scene.fbx(filepath=args.Inobj) 
#bpy.ops.wm.collada_import(filepath=args.Inobj)

# select first object
bpy.context.view_layer.objects.active = bpy.data.objects[0]
bpy.data.objects[0].select_set(True)

context = bpy.context
scene = context.view_layer
obs = [o for o in scene.objects
        if o.type == 'MESH']
        
if len(obs) > 1:
    # clear prior selection
    for o in context.selected_objects:
        o.select_set(False)
    for o in obs:
        o.select_set(True)
    scene.objects.active = obs[0]
    bpy.ops.object.join()
	
    bpy.ops.object.transform_apply(scale = True)
##bpy.ops.object.shade_flat()
bpy.ops.object.transform_apply(scale = True)

## New Code by Abdul

# bpy.ops.object.select_all(action='SELECT')
#sel = bpy.context.selected_objects
#act = bpy.context.active_object

# for obj in sel:
    # if obj.type in 'MESH':
        # bpy.context.view_layer.objects.active = obj
        # bpy.ops.object.modifier_add(type='DECIMATE')
        # bpy.context.object.modifiers["Decimate"].ratio = 0.9

#bpy.context.scene.objects.active = act

bpy.ops.object.select_all(action='DESELECT')

# export scene

if flag:
	bpy.ops.file.pack_all()
	bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.ops.export_scene.fbx(filepath=args.Outfbx,object_types={'MESH'},path_mode='COPY',embed_textures=True)	

outputFilesDirectory = os.getcwd() + '\\outputFiles'
for folder in os.listdir(outputFilesDirectory):
	if os.path.isdir(os.getcwd() + '\\outputFiles\\' +folder):
		shutil.rmtree(os.getcwd() + '\\outputFiles\\' +folder)

