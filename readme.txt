python3.x
Ubuntu tested

Purpose:
	Auto download/setup/install/config of programs upon fresh installation of ubuntu. To ensure all programs, python 3rd party modules, and configs are completed and not forgotted, one command to do it all.


Configurations:
	geany IDE config
	
Python 3rd party modules installed for both python3.x and 2.x. Links to downloads do not search out latest patches/updates/versions yet. But all current versions installed support python3.x. If you want to update a link, in "mysetup.py", under the dictionary packages_dict,  replace the link value with the neew one.
	pygame
	pyglet
	PyOpenGL
	selenium
	bottle
	BeautifulSoup4
	tk
	PyQt4
	pymunk
	PyMySQL
	sympy
	pillow
	django
	fbconsole
	pyside
	numpy
	scipy
	matplotlib
	
	Python2.x only installs:
		mechanize
		cx-freeze
		nmap
		mysqldb
		flask
		gtk2
		

	
Ubuntu repos installed:
python-pyside python3-pyside python-numpy python3-numpy python3-scipy python-scipy python-nmap python-matplotlib python3-matplotlib python-mysqldb python-flask python-gtk2 python-mechanize cx-freeze gparted python-pygame python-bs4 python3-bs4 openjdk-6-jdk openjdk-7-jdk vlc hwinfo python-dev xchat wine winetricks python-tk python3-tk k3b unetbootin tor eclipse nautilus-open-terminal libqt4-dev python-qt4 python3-pyqt4 git git-core git-gui git-doc python-pygame curl openbox obconf obmenu 
openbox-xdgmenu nitrogen grub-customizer mumble weechat weechat-curses terminator tmux ssh gufw gimp gmountiso deluge rtorrent nmap skype apache2 python-pip filezilla screen ghex firefox 
google-chrome-stable epiphany-browser steam blender desmume zsnes htop vim gconf-editor unity-tweak-tool dropbox

Basic installs:
	minecraft
		downloads minecraft.jar
		if beautifulsoup installed upon execution: will download latest mcpatcher from github
	
non-auto files:
	sudo bash watermark_remove.sh (for ubuntu 13.04 AMD hardware unsupported water mark)
	reboot
