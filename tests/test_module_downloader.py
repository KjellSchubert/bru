import unittest
import brulib.module_downloader
import os
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

    def test_get_urls(self):
        formula = {
            'module': 'test_module',
            'version': '0.1alpha1',
            'url': 'https://github.com/KjellSchubert/koa/archive/0.3.tar.gz'
        }
        brulib.module_downloader.get_urls(formula, os.path.join(temp_root, 'bru_modules'))
        assert os.path.exists(os.path.join(temp_root, 'bru_modules', 
            'test_module', '0.1alpha1', 'koa-0.3', 'readme.md'))