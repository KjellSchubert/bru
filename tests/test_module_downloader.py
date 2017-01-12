import unittest
import brulib.module_downloader
import os
import pdb
import shutil

temp_root = './temp_module_downloader'

class LibraryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

    def test_get_urls_tar_gz(self):
        library = brulib.library.Library('./library')
        formula = {
            'module': 'test_module',
            'version': '0.1alpha1',
            'url': 'https://github.com/KjellSchubert/koa/archive/0.3.tar.gz'
        }
        brulib.module_downloader.get_urls(library, formula, 
            os.path.join(temp_root, 'bru_modules'))
        assert os.path.exists(os.path.join(temp_root, 'bru_modules', 
            'test_module', '0.1alpha1', 'koa-0.3', 'readme.md'))

    def test_get_urls_patches(self):
        """ very few packages need a 'patch' consisting of a tar.gz that's
            unpacked on top of an official release. Currently 
            library/ogg/1.3.2.bru is one such example (where the tgz contains
            canned (and trivial) ./configure output).
        """
        library = brulib.library.Library('./library')
        formula = library.load_formula('ogg', '1.3.2')
        brulib.module_downloader.get_urls(library, formula, 
            os.path.join(temp_root, 'bru_modules'))
        # assert library/ogg/1.3.2-config.tar.gz was unpacked at the expected
        # location:
        assert os.path.exists(os.path.join(temp_root, 'bru_modules', 
            'ogg', '1.3.2', 'libogg-1.3.2', 'include', 'ogg', 'config_types.h'))
        # and assert the main tar.gz was unpacked as well:
        assert os.path.exists(os.path.join(temp_root, 'bru_modules', 
            'ogg', '1.3.2', 'libogg-1.3.2', 'src'))

