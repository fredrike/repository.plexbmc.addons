""" addons.xml generator """
import warnings
warnings.filterwarnings("ignore")
import os
import md5
import xml.dom.minidom
import zipfile
import glob
import shutil


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__( self ):
        # generate files
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
        print "Finished updating addons xml and md5 files"

    def _generate_addons_file( self ):
        # addon list
        addons = os.listdir( "." )
        # final addons text
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                # skip any file or .svn folder
                if ( not os.path.isdir( addon ) or addon == ".svn" or addon == ".git" ): continue
                # create path
                _path = os.path.join( addon, "addon.xml" )
                if not os.path.isfile(_path): continue
                # split lines for stripping
                xml_lines = open( _path, "r" ).read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    # add line
                    addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception, e:
                # missing or poorly formatted addon.xml
                print "Excluding %s for %s" % ( _path, e, )
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        # save file
        self._save_file( addons_xml.encode( "UTF-8" ), file="addons.xml" )

    def _generate_md5_file( self ):
        try:
            # create a new md5 hash
            m = md5.new( open( "addons.xml" ).read() ).hexdigest()
            # save file
            self._save_file( m, file="addons.xml.md5" )
        except Exception, e:
            # oops
            print "An error occurred creating addons.xml.md5 file!\n%s" % ( e, )

    def _save_file( self, data, file ):
        try:
            # write data to the file
            open( file, "w" ).write( data )
        except Exception, e:
            # oops
            print "An error occurred saving %s file!\n%s" % ( file, e, )

def recursive_zip(zipf, directory, folder=""):
	for item in os.listdir(directory):
		if not item.endswith(".zip"):
			if os.path.isfile(os.path.join(directory, item)):
				zipf.write(os.path.join(directory, item), folder + os.sep + item, zipfile.ZIP_DEFLATED)
			elif os.path.isdir(os.path.join(directory, item)):
				recursive_zip(zipf, os.path.join(directory, item), folder + os.sep + item)


if ( __name__ == "__main__" ):
    # start
		Generator()
 
		for addon in xml.dom.minidom.parse("addons.xml").getElementsByTagName("addon"):
			name = addon.getAttribute("id") + "-" + addon.getAttribute("version") + ".zip"
			path = addon.getAttribute("id")
			if not os.path.isfile(os.path.join(path,name)):
				print "Creating archive: " + name
				if not os.path.isdir(path):
					os.mkdir(path);
				zipf = zipfile.ZipFile(os.path.join(path, name), "w")
				if os.path.isdir(path + ".git"):
					recursive_zip(zipf, path + ".git", addon.getAttribute("id"))
				else:
					recursive_zip(zipf, path, addon.getAttribute("id"))
				zipf.close()

			if not os.path.isfile(os.path.join(path, "icon.png")):
				if os.path.isfile(os.path.join(path+".git", "icon.png")):
					try:
						shutil.copy(os.path.join(path+".git", "icon.png"), os.path.join(path, "icon.png"))
					except Exception, e:
# oops
						print "%s" % ( e, )
			
			if os.path.isfile(os.path.join(path+".git", "changelog.txt")):
				try:
					shutil.copy(os.path.join(path+".git", "changelog.txt"), os.path.join(path, "changelog-"+addon.getAttribute("version")+".txt"))
				except Exception, e:
# oops
					print "An error occurred creating  %s.\n%s" % ( file, e, )


