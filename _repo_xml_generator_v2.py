""" 
    Put this script in the root folder of your repo and it will
    zip up all addon folders, create a new zip in your zips folder
    and then update the md5 and addons.xml file
"""

import re
import os
import shutil
import hashlib
import zipfile
from xml.etree import ElementTree

def convert_bytes(num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    
    def __init__(self):
        self._remove_binaries()
        print('-----------------------------\n')
        self._create_zips_folder()
        print('-----------------------------\n')
        self._generate_addons_file()
        print('-----------------------------\n')
        self._generate_md5_file()
        print('-----------------------------\n')

    def _remove_binaries(self):
        """
            Removes any and all compiled Python files before operations.
        """
        print("STARTED remove_binaries()")

        for parent, dirnames, filenames in os.walk('.'):
            for fn in filenames:
                if fn.lower().endswith('pyo') or fn.lower().endswith('pyc'):
                    compiled = os.path.join(parent, fn)
                    try:
                        os.remove(compiled)
                        print("Removed compiled python file:")
                        print(compiled)
                        #print('-----------------------------')
                    except:
                        print("Failed to remove compiled python file:")
                        print(compiled)
                        #print('-----------------------------')
            for dir in dirnames:
                if "pycache" in dir.lower():
                    compiled = os.path.join(parent, dir)
                    try:
                        shutil.rmtree(compiled)
                        print("Removed __pycache__ cache folder:")
                        print(compiled)
                        #print('-----------------------------')
                    except:
                        print("Failed to remove __pycache__ cache folder:")
                        print(compiled)
                        #print('-----------------------------')
        print("FINISHED remove_binaries()")

    def _create_zips_folder(self):
        """
            Creates a folder called 'zips', if it doesn't exist already.
            This folder is used to house the repo contents. 
        """
        zips_path = ('zips')
        if not os.path.exists(zips_path):
            os.makedirs(zips_path)    
            print("Created zips folder\n")

    def _create_zip(self, addon_id, version):
        print("STARTED created_zip for addon ", addon_id)

        """
            Creates a zip file in the zips directory for the given addon in each separate directory.
        """
        addon_zip_folder = os.path.join('zips', addon_id)
        addon_src_root = 'src/'

        if not os.path.exists(addon_zip_folder):
            os.makedirs(addon_zip_folder)

        # zip destination of path & filename
        final_zip_filename = os.path.join('zips', addon_id, '{0}-{1}.zip'.format(addon_id, version))

        if not os.path.exists(final_zip_filename):
            print("CREATING ZIP FOR: {0} - version={1}".format(addon_id, version))
            zip = zipfile.ZipFile(final_zip_filename, 'w', compression=zipfile.ZIP_DEFLATED )
            root_len = len(os.path.dirname(os.path.abspath(addon_id)))

            ignore = ['.git', '.github', '.gitignore', '.DS_Store', 'thumbs.db', '.idea', 'venv']
         
            print("current working in path " + os.getcwd())
            os.chdir("src")
            print("current working in path " + os.getcwd())

            for root, dirs, files in os.walk(addon_id):
                # remove any unneeded artifacts
                for i in ignore:
                    if i in dirs:
                        try:
                            dirs.remove(i)
                        except:
                            pass
                    for f in files:
                        if f.startswith(i):
                            try:
                                files.remove(f)
                            except:
                                pass
                
                #changed archive_root to same as root since os.chdir was introduced
                #to solve archive path to exclude src from the zip.
                #archive_root = os.path.abspath(root)[root_len:]
                archive_root = root

                for f in files:
                    fullpath = os.path.join(root, f)
                    
                    archive_name = os.path.join(archive_root, f)

                    print("fullpath of src files " + fullpath)
                    print("archive_name of src files " + archive_name)

                    zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
            
            zip.close()

            ## change back os current working directory to bring pointer back (in case)
            os.chdir("..")
            print("current working in path " + os.getcwd()) 

            #size of new zip file
            size = convert_bytes(os.path.getsize(final_zip_filename))
            print("FINISHED created_zip for addon " + addon_id + " of size " + size)

        self._copy_meta_files(addon_id, addon_zip_folder)
        

    def _copy_meta_files(self, addon_id, addon_folder):
        """
            Copy the addon.xml and relevant art files into the relevant folders in the repository.
        """
        print("STARTED copy_meta_files for addon ", addon_id, ' to folder ', addon_folder)
        
        addon_src_root = "./src"
        tree = ElementTree.parse(os.path.join(addon_src_root, addon_id, 'addon.xml'))
        root = tree.getroot()
               

        copyfiles = ['addon.xml']
        for ext in root.findall('extension'):
            if ext.get('point') == 'xbmc.addon.metadata':
                assets = ext.find('assets')
                for art in assets:
                    copyfiles.append(os.path.normpath(art.text))

        for file in copyfiles:
            addon_path = os.path.join(addon_src_root, addon_id, file)
            zips_path = os.path.join(addon_folder, file)
            asset_path = os.path.split(zips_path)[0] 
            if not os.path.exists(asset_path):
                os.makedirs(asset_path)
            shutil.copy(addon_path, zips_path)
        
        print("FINISHED copy_meta_files for addon ", addon_id)

    def _generate_addons_file(self):
        """
            Generates a zip for each found addon in SRC folder, and updates the addons.xml file accordingly.
        """
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"
        addon_src_root = './src'

        print("STARTED generate_addons_files()")

        for addon in [i for i in os.listdir(addon_src_root) if os.path.isdir(os.path.join(addon_src_root, i))
                                                 and os.path.exists(os.path.join(addon_src_root, i, 'addon.xml'))]:
            try:
                addon_fullpath = os.path.join(addon_src_root, addon)
                _path = os.path.join(addon_fullpath, "addon.xml")

                print ("addon found: ", addon, " full path: ", addon_fullpath, " path exist: ", os.path.exists(_path))

                if not os.path.isdir(addon_fullpath) or not os.path.exists(_path):
                    continue
                xml_lines = open(_path, "r", encoding='utf-8').read().splitlines()
                addon_xml = ""

                # loop thru cleaning each line
                ver_found = False
                for line in xml_lines:
                    if line.find( "<?xml" ) >= 0:
                        continue
                    if 'version="' in line and not ver_found:
                        version = re.compile('version="(.+?)"').findall(line)[0]
                        ver_found = True
                    addon_xml += line.rstrip() + "\n"
                addons_xml += addon_xml.rstrip() + "\n\n"

                # Create the zip files                
                self._create_zip(addon, version)

            except Exception as e:
                print("Excluding {0}: {1}".format(_path, e))

        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        self._save_file(addons_xml.encode('utf-8'), file=os.path.join('zips', 'addons.xml'), decode=True)
        print("Successfully updated addons.xml")
        print("FINISHED generate_addons_files()") 

    def _generate_md5_file(self):
        """
            Generates a new addons.xml.md5 file.
        """
        print("STARTED generated_md5_file")
        try:
            m = hashlib.md5(open(os.path.join('zips', 'addons.xml'), 'r', encoding='utf-8').read().encode('utf-8')).hexdigest()
            self._save_file(m, file=os.path.join('zips', 'addons.xml.md5'))
            print("Successfully updated addons.xml.md5")
        except Exception as e:
            print("An error occurred creating addons.xml.md5 file!\n{0}".format(e))

        print("FINISHED generated_md5_file")

    def _save_file(self, data, file, decode=False):
        """
            Saves a file.
        """
        print("STARTED save_file for ", file)
        try:
            if decode:
                open(file, 'w', encoding='utf-8').write(data.decode('utf-8'))
            else:
                open(file, 'w').write(data)
        except Exception as e:
            print("An error occurred saving {0} file!\n{1}".format(file, e))
        print ("FINISHED save file for ", file)


if __name__ == "__main__":
    Generator()
