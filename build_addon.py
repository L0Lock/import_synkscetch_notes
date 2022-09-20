import shutil
import os
from distutils import dir_util, file_util

# Target folder where to copy the addon's content.
# I use a custom directory to avoid having to reinstall addons at each new Blender version
# If you want to do the same, don't forget to add that path to Blender > Edit menu > Preferences > File Paths tab > Scripts

targetFolder="C:\\AppInstall\\Blender\\MyScripts\\addons\\import_synkscetch_notes\\"
os.makedirs(targetFolder, exist_ok=True)


# Input files and folders. See examples from lines 16 to 19
# Folders will be copied with their full content.
# Put them between '' marks, coma between elements, one per line.
# You can write in absolute and relative paths, I chose relative for simplicity.

inputFiles=['__init__.py',
			'bl_class_registry.py',
			'functions.py',
			'menus.py',
			'operators.py',
			'panels.py',
			'prefs.py',
			]

for src in inputFiles:
	print(f'Copying "{src}" to "{targetFolder}"')
	if os.path.isdir(src):
		dir_util.copy_tree(src, targetFolder, preserve_mode=1, preserve_times=1, preserve_symlinks=0, update=1, verbose=1, dry_run=0)
	elif os.path.isfile(src):
		file_util.copy_file(src, targetFolder, preserve_mode=1, preserve_times=1, update=1, link=None, verbose=1, dry_run=0)
	else:
		print(f'"{src}" not found, skipping...')
		pass