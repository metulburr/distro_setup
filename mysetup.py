#!/usr/bin/env python3

#ubuntu setup script

#things to add
#https://github.com/python-imaging/Pillow donwload and install for pytohn3.x PIL module
#install new video drivers
#download, and install minecraft, dl texture packs, etc.
#https://bitbucket.org/prupe/mcpatcher
#download sublime, setup crack
#donwload and install BeautifulSoup 4 for python 2.x and 3.x
	#http://www.crummy.com/software/BeautifulSoup/

#modify current
#change geany to config colorschemes in
	#vibrant-ink.conf save file to colorschemes
	#~/.config/geany/colorschemes/

#python packages
	#pymunk DONE
	#pyglet DONE
	#PyMySQL DONE
	#PyOpenGL DONE
	#selenium DONE
	#sympy DONE
	#Pillow DONE
	#fbconsole DONE
	#django DONE
	#cx_freeze 2DONE
	#bottle DONE
	
	
import os
import urllib.request
import shutil
import tarfile
import subprocess
import zipfile
import webbrowser

def pygame_install(name):
	#extract tar, directory create is just pygame
	extract(name) 
	#download dependencies
	command(install_packages='python3 python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev')
	os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pygame'))
	print('PRESS ENTER!!!')
	command(cmd='sudo python3 setup.py install')
	os.chdir('..')
	
def python_3rd_party_install(f, stripper=None):
	if not stripper:
		s = '.tar.gz'
	else:
		s = stripper
	extract(f)
	filename = f.split(s)[0] #using this instead of os.path.splitext() because it did not parse some correctly
	fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
	os.chdir(fullpath)
	command(cmd='sudo python3 setup.py install')
	command(cmd='sudo python2 setup.py install')
	os.chdir('..')
		
def geany_install(packages):
	command(install_packages=packages)
	schemepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'schemes')
	#command(cmd='sudo cp {}/* ~/.config/geany/colorschemes/'.format(schemepath))
	new_schemepath = os.path.join(os.environ['HOME'], '.config/geany/colorschemes')
	command(cmd='sudo cp -r {} {}'.format(schemepath, new_schemepath ))
	choice = input('Change geany default to run python3.x instead? [y/n] ')
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
		
def minecraft_install():
	
	#attempt to get latest mcpatcher if beautifulsoup is installed
	try:
		from bs4 import BeautifulSoup
	except ImportError:
		return
	url = 'https://github.com/pclewis/mcpatcher/downloads'
	res = urllib.request.urlopen(url)
	html = res.read().decode()

	soup = BeautifulSoup(html)
	tags = soup.findAll('li', {'class', 'ctype-unknown'})
	urlpath = tags[1].find('a')['href'] #latest jar mcparcher version path

	new_url = 'https://github.com' +  urlpath
	download(new_url)
	
def sublime_install(name):
	extract(name)
	ch = input('Crack Sublime Text 2 to be registered? [Y/N] Input all of license into sublime_test (open) -> Help -> Enter License (including the BEGIN/END license part [Y/N]')
	if ch.lower() == 'y':
		fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Sublime Text 2')
		os.chdir(fullpath)
		command('sudo apt-get install sed')
		command(cmd="sed {} sublime_text > cracked".format(repr(r's/\x33\x42/\x32\x42/g')))
		command(cmd='sudo rm sublime_text')
		command(cmd='mv cracked sublime_text')
		command(cmd='chmod 777 sublime_text')
		os.chdir('..')
		webbrowser.open('license.txt')

def extract(f):
	if tarfile.is_tarfile(f):
		filer = tarfile.open(f)
		print('extracting {}'.format(f))
		filer.extractall()
	elif f.endswith('.zip'):
		zip = zipfile.ZipFile(f)
		print('extracting {}'.format(f))
		zip.extractall()
	
def command(cmd=None, install_packages=None):
	if install_packages:
		cmd = 'sudo apt-get install {}'.format(install_packages)
		installing = True
	else:
		installing = False
	print(cmd)
	proc = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)
	error_string = proc.communicate()[1].decode()
	if error_string:
		print(error_string)
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
		print()
		new = command(install_packages=val)
		if new:
			command(install_packages=new)
	elif keyword == 'minecraft':
		minecraft_install()
	elif keyword == 'pillow':
		python_3rd_party_install(val, '.zip')
	elif keyword == 'pymunk':
		python_3rd_party_install(val, '.zip')
	elif keyword == 'sympy':
		python_3rd_party_install(val, '-py3.2.tar.gz')
	#if keyword == 'sublime':
	#	sublime_install(val)
	else:
		python_3rd_party_install(val)


	
	
	'''
	elif keyword == 'pyglet':
		python_3rd_party_install(val)
	elif keyword == 'pyopengl':
		python_3rd_party_install(val)
	elif keyword == 'sel':
		python_3rd_party_install(val)
	elif keyword == 'cx':
		python_3rd_party_install(val)
	elif keyword == 'bottle':
		python_3rd_party_install(val)
	elif keyword == 'pymysql':
		python_3rd_party_install(val)
	elif keyword == 'django':
		python_3rd_party_install(val)
	elif keyword == 'fbconsole':
		python_3rd_party_install(val)
	'''
		
	
packages_dict = {
	#downloads
	'pygame':'https://launchpad.net/debian/experimental/+source/pygame/1.9.2~pre~r3144-1/+files/pygame_1.9.2~pre~r3144.orig.tar.gz',
	'minecraft':'https://s3.amazonaws.com/MinecraftDownload/launcher/minecraft.jar',
	'pyglet':'http://pyglet.googlecode.com/files/pyglet-1.2alpha1.tar.gz',
	'pyopengl':'https://pypi.python.org/packages/source/P/PyOpenGL/PyOpenGL-3.0.2.tar.gz',
	'sel':'https://pypi.python.org/packages/source/s/selenium/selenium-2.33.0.tar.gz',
	#'cx':'http://downloads.sourceforge.net/project/cx-freeze/4.3.1/cx_Freeze-4.3.1.tar.gz',
	'bottle':'https://pypi.python.org/packages/source/b/bottle/bottle-0.11.3.tar.gz',
	'pymunk':'http://pymunk.googlecode.com/files/pymunk-3.0.0.zip',
	'pymysql':'http://pymysql.googlecode.com/files/PyMySQL3-0.4.tar.gz',
	'sympy':'http://sympy.googlecode.com/files/sympy-0.7.2-py3.2.tar.gz',
	'pillow':'https://pypi.python.org/packages/source/P/Pillow/Pillow-2.0.0.zip',
	'django':'https://pypi.python.org/packages/source/D/Django/Django-1.5.1.tar.gz',
	'fbconsole':'https://pypi.python.org/packages/source/f/fbconsole/fbconsole-0.3.tar.gz',
	#'sublime':'http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.1%20x64.tar.bz2',
	
	#package manager installs
	'geany':'geany geany-plugins',
	'basic':'python-pyside python3-pyside python-numpy python3-numpy python3-scipy python-scipy python-nmap python-matplotlib python3-matplotlib python-mysqldb python-flask python-gtk2 python-mechanize cx-freeze gparted python-pygame python-bs4 python3-bs4 openjdk-6-jdk openjdk-7-jdk vlc hwinfo python-dev xchat wine winetricks python-tk python3-tk k3b unetbootin tor eclipse nautilus-open-terminal libqt4-dev python-qt4 python3-pyqt4 git git-core git-gui git-doc python-pygame curl openbox obconf obmenu openbox-xdgmenu nitrogen grub-customizer mumble weechat weechat-curses terminator tmux ssh gufw gimp gmountiso deluge rtorrent nmap skype apache2 python-pip filezilla screen ghex firefox google-chrome-stable epiphany-browser steam blender desmume zsnes htop vim gconf-editor unity-tweak-tool dropbox',
	#'basic':'man-db non-existing-package non-existing-package2 non-existing-package3 man-db'
}

for key, val in packages_dict.items():
	if val.startswith('http'):
		name = download(val)
		setup(key, name)
	else:
		setup(key, val)
print('Program Complete')


