import unittest
import brulib.install
import brulib.library
import os
import pdb
import shutil

temp_root = 'temp_install'
install = brulib.install

def rmTempTestDir():
    if os.path.exists(temp_root):
        shutil.rmtree(temp_root)

class InstallTestCase(unittest.TestCase):

    def setUp(self):
        rmTempTestDir()

    def tearDown(self):
        rmTempTestDir()

    def test_get_single_bru_file(self):

        bru_file = install.get_single_bru_file(temp_root)
        self.assertEqual(bru_file, None) # assuming dir was empty
        
        bru_file = install.get_or_create_single_bru_file(temp_root)
        expected_file = os.path.join('temp_install', 'package.bru')
        self.assertEqual(bru_file, expected_file)
        
        bru_file = install.get_single_bru_file(temp_root)
        self.assertEqual(bru_file, expected_file) # assuming dir was empty
        
        os.remove(expected_file)

    def test_parse_module_at_version(self):
        self.assertEqual(
            install.parse_module_at_version('googlemock@1.7.0'),
            install.Installable('googlemock', '1.7.0'))
        self.assertEqual(
            install.parse_module_at_version('googlemock'),
            install.Installable('googlemock', None))
            
    def test_parse_existing_module_at_version(self):
        library = brulib.library.Library('./library')

        self.assertEqual(
            install.parse_existing_module_at_version('googlemock@1.7.0', library),
            install.Installable('googlemock', '1.7.0'))
        self.assertEqual(
            install.parse_existing_module_at_version('googlemock', library),
            install.Installable('googlemock', '1.7.0'))
        # that's assuming the latest version of googlemock in ./library
        # is still 1.7.0
        
        self.assertRaises(Exception, 
            lambda: install.parse_module_at_version('nonexistingmodule', library))
        self.assertRaises(Exception, 
            lambda: install.parse_module_at_version('googlemock@0.1', library))
        # there should be no googlemock 0.1 in the ./library

    def test_add_dependencies_to_bru(self):
        bru_file = os.path.join(temp_root, 'test_add_deps.bru')
        brulib.jsonc.savefile(bru_file, {})
        install.add_dependencies_to_bru(
            bru_file,
            [install.Installable('protobuf', '99.0')])
        for i in range(2):
            install.add_dependencies_to_bru(
                bru_file,
                [install.Installable('googlemock', '1.7.0')])
        formula = brulib.jsonc.loadfile(bru_file)
        self.assertEqual(formula['dependencies'], {
            'googlemock': '1.7.0',
            'protobuf': '99.0'
        })

    def test_add_dependencies_to_gyp(self):
        gyp_file = os.path.join(temp_root, 'test_add_deps.gyp')
        install.create_gyp_file(gyp_file)
        install.add_dependencies_to_gyp(
            gyp_file,
            [install.Installable('protobuf', '99.0')])
        for i in range(2):
            install.add_dependencies_to_gyp(
                gyp_file,
                [install.Installable('googlemock', '1.7.0')])
        gyp = brulib.jsonc.loadfile(gyp_file)
        first_target = gyp['targets'][0]
        deps = first_target['dependencies']
        self.assertEqual(len(deps), 2) # no dups
        self.assertEqual(
            set(deps),
            set([
                'bru_modules/googlemock/googlemock.gyp:*',
                'bru_modules/protobuf/protobuf.gyp:*',
            ]))
    
    def test_exec_make_command(self):
        platform = "Linux"
        formula = {
            'module': 'foo',
            'version': '0.1alpha',
            'make_command': {
                platform: 'echo "hello" > foo.txt' # silly cmd, just for testing
            }
        }
        # mkdir because exec_make_command expects that the targz alrdy has
        # been extracted into the module dir before invoking the make_command
        # (e.g. ./configure)
        module_dir = os.path.join(temp_root, formula['module'], formula['version'])
        os.makedirs(module_dir)
        install.exec_make_command(formula, temp_root, platform)
        
        # verify cmd was executed with the expected cwd:
        assert os.path.exists(os.path.join(module_dir, 'foo.txt'))

    def test_resolve_conflicts(self):
        library = brulib.library.Library('./library')
        # we could create a library mock that actually needs to resolve
        # some conflicts, but I'm not bothering with that for now:
        deps = {
            'boost-assert': '1.57.0',
            'zlib': '1.2.8'
        }
        resolved = install.resolve_conflicts(library, deps, 'test.bru')
        
        # verify the transitive hull of dependencies looks as expected:
        self.assertEqual(
            set(resolved),
            set([
                ('zlib', '1.2.8', 'test.bru'), 
                ('boost-assert', '1.57.0', 'test.bru'), 
                ('boost-config', '1.57.0', 'boost-assert')]))

    def test_install_zlib(self):
        """ tests 'bru install zlib', which is one of the simplest cases """
        
        # this test will write to './bru_modules/zlib', let's delete this
        # since otherwise the (alrdy completed) install will be skipped.
        # TODO: make bru_modules_root a cmd_install() param?
        zlib_module_dir = os.path.join('bru_modules', 'zlib')
        if os.path.exists(zlib_module_dir):
            shutil.rmtree(zlib_module_dir)
            
        library = brulib.library.Library('./library')
        install.cmd_install(library, ['zlib'])
        install.cmd_install(library, []) # should be a NOP
        assert os.path.exists(zlib_module_dir)
        assert os.path.exists(os.path.join(zlib_module_dir, 'zlib.gyp'))
