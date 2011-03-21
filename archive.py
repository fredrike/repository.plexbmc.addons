#import pprint
import xml.dom.minidom
import zipfile
import glob, os
#from xml.dom.minidom import Node

def recursive_zip(zipf, directory, folder=None):
	print directory
	nodes = os.listdir(directory)

	for item in nodes:
#		if not item.endswith(".zip"):
			if os.path.isfile(item):
				print "i"+item
				zipf.write(item, folder, zipfile.ZIP_DEFLATED)
			elif os.path.isdir(item):
				print "d"+item
				recursive_zip(zipf, os.path.join(directory, item), item)

for addon in xml.dom.minidom.parse("addons.xml").getElementsByTagName("addon"):
#	print addon.getAttribute("version")
	name = addon.getAttribute("id") + "-" + addon.getAttribute("version")
	print name
	zipf = zipfile.ZipFile(addon.getAttribute("id") + "/" + name + ".zip", "w")
	path = "./"+addon.getAttribute("id")+"/"
	print path
	path = "plugin.video.plexbmc/"
	recursive_zip(zipf, path)
	zipf.close()

#
#for name in glob.glob("*"):
#	file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
#	print name + os.path.basename(name)
#file.close()
#

