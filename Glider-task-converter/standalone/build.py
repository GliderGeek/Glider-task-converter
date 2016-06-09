import sys
import os
import platform
import shutil
sys.path.append('../')
from Tkinter import Label, Tk, Button, Entry, W, E
import subprocess
from contextlib import contextmanager

version=0.50
main_file = "main"

root = Tk()

def correct_version():
	print 'Build process continues with version %s' % version
	
	if platform.system() == 'Darwin':
		platform_name = "mac"
		source_executable = main_file
		executable = "Glider-task-converter_mac.app"	
		
		subprocess.call(["pyinstaller", "--onefile", "--windowed", os.path.join("..", main_file+".py")])
		
	elif platform.system() == 'Windows':
		platform_name = "windows"
		source_executable = main_file + ".exe"
		executable = "Glider-task-converter_windows.exe"
	
		subprocess.call(["pyinstaller", "-F", "--noconsole", os.path.join("..", main_file+".py")])	
		
	elif platform.system() == "Linux":
		platform_name = 'linux'
		source_executable = main_file
		executable = "Glider-task-converter_linux"
		
		subprocess.call(["pyinstaller", "-F", os.path.join("..", main_file+".py")])
	
	# create platform folder. if already exists, remove executable
	if not os.path.exists(platform_name):
		os.makedirs(platform_name)
	else:
		if platform.system() == "Darwin":
			if os.path.exists(os.path.join(platform_name, executable+".app")):
				shutil.rmtree(os.path.join(platform_name, executable+".app"))
		else:
			if os.path.exists(os.path.join(platform_name, executable)):
				os.remove(os.path.join(platform_name, executable))			
	
	foldername = "%s_v%s" % (platform_name, version)
	os.makedirs(foldername)
	
	# delete zip file if it exists
	if os.path.exists("%s.zip" % foldername):
		os.remove("%s.zip" % foldername)
	
	# copy executable to zip folder and platform_folder
	if platform.system() == 'Darwin':
		shutil.copytree(os.path.join("dist", source_executable+".app"), os.path.join(foldername, executable))
		shutil.move(os.path.join("dist", source_executable+".app"), os.path.join(platform_name, executable))
	else:  # linux and windows
		shutil.copy(os.path.join("dist", source_executable), os.path.join(foldername, executable))
		shutil.move(os.path.join("dist", source_executable), os.path.join(platform_name, executable))
	
	# move pdf to zip folder and create zip file
	shutil.make_archive(foldername,"zip",foldername)
	
	# remove unnecessary folders and files
	shutil.rmtree(foldername)
	shutil.rmtree('build')
	shutil.rmtree('dist')
	os.remove("main.spec")	
	
	root.quit()
	    
def incorrect_version():
	print 'Build process is cancelled because of incorrect version number'
	root.quit()

version_title = Label(root, text='Glider-task-converter %s' %version, font=("Helvetica", 30))
question = Label(root, text="Is this the correct version number?", font=("Helvetica", 12))
stop = Button(root, command=incorrect_version, text='no')
go_on = Button(root, command=correct_version, text='yes')

version_title.grid(row=0, column=0, columnspan=2)
question.grid(row=1, column=0, columnspan=2)
stop.grid(row=2, column=0, sticky=E)
go_on.grid(row=2, column=1, sticky=W)

root.mainloop()
