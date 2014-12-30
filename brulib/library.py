""" Helpers for accessing files in the ./library dir.
    This dir has a $module/$version.bru+gyp structure, containing information
    about how to download tar.gzs for (or hwo to clone) each module, as well
    as for how to build the module's libs and some of its tests/examples.
"""
import os
import re
import functools
import brulib.jsonc

def alphnumeric_lt(a, b):
    """ helper func for module version comparison """
    # from http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    def to_alphanumeric_pairs(text):
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return alphanum_key(text)
    return to_alphanumeric_pairs(a) < to_alphanumeric_pairs(b)

@functools.total_ordering
class ModuleVersion:
    """ helper class for module version comparison """
    def __init__(self, version_text):
        self.version_text = version_text
    def __lt__(self, other):
        lhs = self .version_text
        rhs = other.version_text
        # module versions could be straightforward like 1.2.3, or they could be
        # openssl-style mixtures of numberrs & letters like 1.0.0f
        return alphnumeric_lt(lhs, rhs)

class Library:
    """ Gives access to content of ./library, getting information about modules 
        and versions
    """
    
    def __init__(self, library_rootdir):
        """ param library_rootdir e.g. './library' """
        self._library_rootdir = library_rootdir
        
    def get_root_dir(self):
        """ return ctor param """
        return self._library_rootdir

    def get_module_dir(self, module_name):
        """ get the dir containing the *.bru and other files for this module,
            so return a subdir of get_root_dir().
        """
        module_dir = os.path.join(self.get_root_dir(), module_name)
        return module_dir

    def _load_from_library(self, module_name, module_version, ext):
        """ ext e.g. '.bru' or '.gyp' """
        json_file_name = os.path.join(self.get_module_dir(module_name), module_version + ext)
        jso = brulib.jsonc.loadfile(json_file_name)
        return jso
    
    def has_formula(self, module_name, module_version):
        # lame impl: throw needless exception if module doesn't exist. Revise?
        try:
            self.load_formula(module_name, module_version)
            return True
        except:
            return False
    
    def load_formula(self, module_name, module_version):
        """ E.g. to load recipe for module_name='zlib' module_version='1.2.8' """
        # Recipes will be downloaded from some server some day (e..g  from github
        # directly).
        formula = self._load_from_library(module_name, module_version, '.bru')
        assert formula['module'] == module_name and formula['version'] == module_version
        return formula
    
    def load_gyp(self, formula):
        """ to load the gyp file associated with a formula """
        gyp = self._load_from_library(formula['module'], formula['version'], '.gyp')
        assert 'targets' in gyp # otherwise it's not a (or is an empty) gyp file
        return gyp
    
    def _save_to_library(self, formula, jso, ext):
        """ param jso is the dict or OrderedDict to save, which can by the
            forumula itself, or a gyp file, or ... """
        module_version = formula['version']
        module_dir = self.get_module_dir(formula['module'])
        file_name = os.path.join(module_dir, module_version + ext)
        brulib.jsonc.savefile(file_name, jso)
        #print("not modifying existing " + bru_file_name)
    
    def save_formula(self, formula):
        """ param formula is the same dict as returned by load_formula,
            so should be an OrderedDict.
        """
        self._save_to_library(formula, formula, '.bru')
    
    def save_gyp(self, formula, gyp):
        """ param is a dict representing gyp file content """
        self._save_to_library(formula, gyp, '.gyp')
    
    def get_all_versions(self, module):
        """ yield all known versions of a module """
        bru_file_names = os.listdir(self.get_module_dir(module))
        regex = re.compile('^(.+)\\.bru$') # version can be 1.2.3 or 1.2rc7 or ...
        for bru_file_name in bru_file_names:
            match = regex.match(bru_file_name)
            if match != None:
                version = match.group(1)
                yield version
    
    def get_latest_version_of(self, module):
        """ return the latest version of a module using alphanumeric comparison
            of version strings. So this works fine for versions like '3.2.1'
            but not as well when comparing '3.2.1rc1' with '3.2.1beta7'
        """
        versions = self.get_all_versions(module)
        return max((ModuleVersion(version_text) for version_text in versions)).version_text
    

