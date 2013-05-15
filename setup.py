#!/usr/bin/env python3

#things to add
#https://github.com/python-imaging/Pillow donwload and install for pytohn3.x PIL module
#update server to Rochester NY
#install new video drivers
#download, and install minecraft, dl texture packs, etc.

import os
import urllib.request
import shutil
import tarfile
import subprocess

def pygame_install(name):
	#extract tar, directory create is just pygame
	extract(name) 
	#download dependencies
	command(install_packages='python3 python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev')
	os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pygame'))
	command(cmd='sudo python3 setup.py install')
		
def geany_install(packages):
	command(install_packages=packages)
	choice = input('Use python3 for geany run command default? [y/n] ')
	if choice.lower() == 'y':
		fullpath = '/usr/share/geany/filetypes.python'
		print('modifying {}'.format(fullpath))
		
		f = open(fullpath)
		file_list = f.readlines()
		for line in file_list:
			ind = file_list.index(line)
			if 'compiler=' in line:
				file_list[ind] = 'compiler=python3 -m py_compile "%f"\n'
			elif 'run_cmd' in line:
				file_list[ind] = 'run_cmd=python3 "%f"\n'

		command('sudo rm {}'.format(fullpath))
		name = os.path.split(fullpath)[1]
		path = os.path.split(fullpath)[0]
		print('creating new {}'.format(name))
		new = open(name, 'w')
		for line in file_list:
			new.write(line)
		new.close()
		command(cmd='sudo mv {} {}'.format(name, path))
		
			

def extract(f):
	filer = tarfile.open(f)
	if tarfile.is_tarfile(f):
		print('extracting {}'.format(f))
		filer.extractall()


	
def command(cmd=None, install_packages=None):
	if install_packages:
		cmd = 'sudo apt-get install {}'.format(install_packages)
		installing = True
	else:
		installing = False
	print(cmd)
	proc = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)
	error_string = proc.communicate()[1].decode()
	if installing and error_string:
		package_remove = []
		error_list = error_string.split('\n')
		for error in error_list:
			if 'Unable to locate package' in error:
				package_remove.append(error.split()[-1])
			print(error)
			
		proc.wait()

		for bad_package in package_remove:
			install_packages = install_packages.replace(bad_package, '', 1)
			
		return install_packages
	else:
		proc.wait()

def download(url):
	req = urllib.request.urlopen(url)
	filename = os.path.split(url)[1]
	print('downloading {}'.format(filename))
	with open(filename,'wb') as f:
		shutil.copyfileobj(req,f)
	return filename
		
def setup(keyword, val=None):
	print('setting up {}'.format(keyword))
	if keyword == 'pygame':
		pygame_install(val) #val == filename
		print('pygame installation complete')
	elif keyword == 'geany':
		geany_install(val)
		print('geany installation complete')
	elif keyword == 'basic':
		new = command(install_packages=val)
		if new:
			command(install_packages=new)
		
		
	
packages_dict = {
	#downloads
	'pygame':'https://launchpad.net/debian/experimental/+source/pygame/1.9.2~pre~r3144-1/+files/pygame_1.9.2~pre~r3144.orig.tar.gz',
	
	#package manager installs
	'geany':'geany geany-plugins',
	'basic':'gparted openjdk-6-jdk openjdk-7-jdk vlc hwinfo python-dev xchat wine winetricks python-tk python3-tk k3b unetbootin tor eclipse nautilus-open-terminal libqt4-dev python-qt4 python3-pyqt4 git git-core git-gui git-doc python-pygame curl openbox obconf obmenu openbox-xdgmenu nitrogen grub-customizer mumble weechat weechat-curses terminator tmux ssh gufw gimp gmountiso deluge rtorrent nmap skype apache2 python-pip filezilla screen ghex firefox google-chrome-stable epiphany-browser steam blender desmume zsnes htop vim gconf-editor unity-tweak-tool',
	#'basic':'man-db non-existing-package non-existing-package2 non-existing-package3 man-db'
}

for key, val in packages_dict.items():
	if val.startswith('http'):
		name = download(val)
		setup(key, name)
	else:
		setup(key, val)


