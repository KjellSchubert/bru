import unittest
import brulib.library
import os
import shutil

temp_root = './temp_library'

class LibraryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # create a temp library root:
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(temp_root)

    def test_save_load_formula_and_gyp(self):
        
        lib = brulib.library.Library(temp_root)
        
        # formula aka the content of a *.bru file
        formula = {
            'module': 'foo',
            'version': '0.1'
        }
        lib.save_formula(formula)
        assert lib.has_formula(formula['module'], formula['version'])
        assert not lib.has_formula(formula['module'], '0.2')
        self.assertEqual(formula, 
            lib.load_formula(formula['module'], formula['version']))
        
        gyp = { 'targets': [{
                'target': {
                    'target_name': 'foolib',
                    'type': 'executable'
                }
            }
        ]}
        lib.save_gyp(formula, gyp)
        self.assertEqual(gyp, lib.load_gyp(formula))

    def test_get_latest_version(self):

        lib = brulib.library.Library(temp_root)
        lib.save_formula({'module': 'foo', 'version': '0.1'})
        lib.save_formula({'module': 'foo', 'version': '2.6'})
        lib.save_formula({'module': 'foo', 'version': '11.1'})
        self.assertEqual(
            set(lib.get_all_versions('foo')), 
            set(['0.1', '2.6', '11.1']))
        self.assertEqual(lib.get_latest_version_of('foo'), '11.1')

    def test_alphanumeric(self):
        alphnumeric_lt = brulib.library.alphnumeric_lt
        assert alphnumeric_lt('0.1', '0.2')
        assert not alphnumeric_lt('0.2', '0.1')
        assert not alphnumeric_lt('0.2', '0.2')
        assert not alphnumeric_lt('0', '0')
        assert alphnumeric_lt('1', '2')
        assert alphnumeric_lt('0.0.0.0.1', '0.0.0.0.2')
        assert alphnumeric_lt('1.5rc1', '1.5rc2')

    def test_ModuleVersion(self):
        ModuleVersion = brulib.library.ModuleVersion
        assert ModuleVersion('0.1') < ModuleVersion('0.2')
        #? assert ModuleVersion('0.1') == ModuleVersion('0.1')
        assert ModuleVersion('0.2') > ModuleVersion('0.1')