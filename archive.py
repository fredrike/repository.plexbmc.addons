import xml.dom.minidom
import zipfile
import glob, os

def recursive_zip(zipf, directory, folder=""):
	for item in os.listdir(directory):
		if not item.endswith(".zip"):
			if os.path.isfile(os.path.join(directory, item)):
				zipf.write(os.path.join(directory, item), folder + os.sep + item, zipfile.ZIP_DEFLATED)
			elif os.path.isdir(os.path.join(directory, item)):
				recursive_zip(zipf, os.path.join(directory, item), folder + os.sep + item)

for addon in xml.dom.minidom.parse("addons.xml").getElementsByTagName("addon"):
	name = addon.getAttribute("id") + "-" + addon.getAttribute("version") + ".zip"
	print "Creating archive: " + name
	zipf = zipfile.ZipFile(os.path.join(addon.getAttribute("id"), name), "w")
	path = addon.getAttribute("id")
	recursive_zip(zipf, path, addon.getAttribute("id"))
	zipf.close()

#
#for name in glob.glob("*"):
#	file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
#	print name + os.path.basename(name)
#file.close()
#

