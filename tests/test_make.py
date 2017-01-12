import unittest
import brulib.install
import brulib.make
import brulib.runtests
import brulib.library
import os
import pdb
import shutil

temp_root = 'temp_test'

def rmTempTestDir():
    if os.path.exists(temp_root):
        shutil.rmtree(temp_root)

class MakeTestCase(unittest.TestCase):

    def setUp(self):
        rmTempTestDir()

    def tearDown(self):
        rmTempTestDir()

    def test_make_tinyjs(self):
        library = brulib.library.Library('./library')
        brulib.install.cmd_install(library, ['tiny-js'])
        config = 'Debug'
        verbose = 0
        brulib.make.cmd_make(config, verbose)
        # assert that built products are in out/Release or in ./Release
        # The tiny-js-test is the target_name as specified in tiny-js's *.gyp.
        assert brulib.runtests.locate_executable('tiny-js-test')
        
        # since we alrdy bothered building these modules let's test them 
        # as well:
        brulib.runtests.cmd_test(['tiny-js'])
        brulib.runtests.cmd_test([]) # runs tests for all modules
