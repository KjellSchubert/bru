#!/usr/bin/env python3

import json
import itertools
import collections
import urllib.request
import urllib.parse # python 2 urlparse
import re
import os
import os.path
import platform
import shutil
import subprocess
import glob
import time
import argparse
from enum import Enum
import pdb # only if you want to add pdb.set_trace()

import brulib.jsonc
import brulib.library
import brulib.install

# http://stackoverflow.com/questions/4934806/python-how-to-find-scripts-directory
def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_library_dir():
    """ assuming we execute bru.py from within its git clone the library
        directory will be located in bru.py's base dir. This func here
        returns the path to this library dir. """
    return os.path.join(get_script_path(), 'library')

def get_library():
    return brulib.library.Library(get_library_dir())

def get_test_targets(gyp):
    """ returns the subset of gyp targets that are tests """

    # Each module typically declares a static lib (usually one, sometimes
    # several), as well as one or more tests, and in rare cases additional
    # executables, e.g. as utilities.
    # How can we tell which of the targets are tests? Heuristically static libs
    # cannot be tests, executables usually but not always are. What many tests
    # still need though is a cwd at startup (e.g. to find test data), which
    # differs from module to module. Let's add this test/cwd property to the
    # gyp target, gyp will ignore such additional props silently. This test/cwd
    # is interpreted relative to the gyp file (like any other path in a gyp file).
    targets = gyp['targets']
    for target in targets:
        if 'test' in target:
            yield target

class TestResult(Enum):
    fail = 0
    success = 1
    notrun = 2 # e.g. not run because executable wasnt built or wasnt found

class CompletedTestRun:
    def __init__(self, target_name, test_result):
        """ param test is a gyp target name for given module, e.g. 'googlemock_test'
            param result is a test result
            param result is of type TestResult
        """
        self.target_name = target_name
        self.test_result = test_result
        self.module = None
        self.duration_in_ms = -1 # -1 means test wasnt run yet

def locate_executable(target_name):
    """ return None if it (likely) wasnt built yet (or if for some other reason
        we cannot determine where the executable was put by whatever toolchain
        gyp was triggering.
        Otherwise return relative path to executable.
    """
    for config in ['Release', 'Debug']:
        candidates = [
            os.path.join('out', config, target_name),
            os.path.join('out', config, target_name + '.exe'),
            os.path.join(config, target_name),
            os.path.join(config, target_name + '.exe')]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
    return None

def exec_test(gypdir, target):
    """ runs test (if executable was built) and returns an instance of
        CompletedTestRun.
        param gypdir is the location of the gyp file
        param target is a 'target' node from a gyp file, so a dict with
              keys like gyp's 'target_name' and the bru-specific 'test'
    """

    # Now knowing the target we have the following problems:
    # * where is the compiled target executable located? E.g. on Ubuntu
    #   with make I find it in out/Release/googlemock_test but on Windows
    #   with msvs it ends in Release/googlemock_test.exe
    # * run Debug or Release or some other config? Let's run Release only
    #   for now. TODO: make configurable, or use Release-Debug fallback?
    #   Or run whichever was built last?
    target_name = target['target_name']
    exe_path = locate_executable(target_name)
    if exe_path != None:
        print('running', target_name)
        t0 = time.time() # or clock()?
        test = target['test']
        rel_cwd = test['cwd'] if 'cwd' in test else './'
        test_argv = test['args'] if 'args' in test else []
        test_stdin = test['stdin'] if 'stdin' in test else None
        proc = subprocess.Popen([os.path.abspath(exe_path)] + test_argv,
                                cwd = os.path.join(gypdir, rel_cwd),
                                stdin = subprocess.PIPE if test_stdin != None else None)
        if test_stdin != None:
            # from http://stackoverflow.com/questions/163542/python-how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument
            proc.stdin.write(test_stdin.encode('utf8'))
            proc.stdin.close() # signal eos ?
            proc.communicate() # necessary ?
        proc.wait()
        returncode = proc.returncode
        duration_in_ms = int(1000 * (time.time() - t0))
        print(target_name, 'returned with exit code', returncode, 'after',
            duration_in_ms, 'ms')
        testrun = CompletedTestRun(target_name,
            TestResult.success if returncode == 0 else TestResult.fail)
        testrun.duration_in_ms = duration_in_ms
        return testrun
    else:
        print('cannot find executable', target_name)
        return CompletedTestRun(target_name, TestResult.notrun)

def collect_tests(module_names):
    """ yields tuples (module, gypdir, test_target), where gypdir is the
        directory the *gyp file is located in (since all file paths in the
        gyp - e.g. the test.cwd - are relative to that particular dir """
    modules_dir = 'bru_modules'
    for module in module_names:
        gypdir = os.path.join(modules_dir, module)
        gyp = brulib.jsonc.loadfile(os.path.join(
                gypdir, module + ".gyp"))
        test_targets = get_test_targets(gyp)
        for test_target in test_targets:
            yield (module, gypdir, test_target)

def cmd_test(testables):
    """ param testables is list of module names, empty to test all modules
    """

    # You alrdy can run tests for upstream deps via these cmds, here
    # for example for running zlib tests:
    #   >bru install
    #   >cd bru_modules/zlib
    #   >gyp *.gyp --depth=.
    #   >make
    #   >out/Default/zlib_test
    # This command here is supposed to automate these steps: you can run these
    # commands here:
    #   >bru test  # runs tests for all modules in ./bru_modules
    #   >bru test boost-regex  # runs tests for given modules only

    modules_dir = 'bru_modules'
    if len(testables) == 0:
        for gyp_filename in glob.glob(os.path.join(modules_dir, '**', '*.gyp')):
            module_dir = os.path.dirname(gyp_filename)
            _, module = os.path.split(module_dir)
            testables.append(module)

    # first let's check if all tests were built already, if they weren't then
    # we'll do an implicit 'bru make' before running tests
    def did_all_builds_complete(testables):
        for module, gypdir, target in collect_tests(testables):
            target_name = target['target_name']
            if locate_executable(target_name) == None:
                print("executable for {}:{} not found".format(
                    module, target_name))
                return False
        return True
    if not did_all_builds_complete(testables):
        print("running 'bru make':")
        cmd_make()

    testruns = []
    module2test_count = dict((module, 0) for module in testables)
    for module, gypdir, target in collect_tests(testables):
        testrun = exec_test(gypdir, target)
        testrun.module = module
        testruns.append(testrun)
        module2test_count[module] += 1
        
    # for modules that don't have tests defined yet strive for adding
    # some tests, warn/inform the user about these modules here:
    modules_without_tests = [module 
                for (module, test_count) in module2test_count.items()
                if test_count == 0]

    # also partition/group testruns by test result:                
    testgroups = {} # testresult to list of testruns, so partitioned testruns
    for test_result, runs in itertools.groupby(testruns,
                             lambda testrun: testrun.test_result):
        testgroups[test_result] = list(runs)

    def get_test_group(test_result):
        return testgroups[test_result] if test_result in testgroups else []

    def print_test_group(msg, test_result):
        testgroup = list(get_test_group(test_result))
        if len(testgroup) > 0:
            print(msg.format(len(testgroup)))
            for testrun in testgroup:
                line = '  {}:{}'.format(testrun.module, testrun.target_name)
                if testrun.duration_in_ms >= 0:
                    line += ' after {} ms'.format(testrun.duration_in_ms)
                print(line)
        return len(testgroup)

    print("test summary:")
    if len(modules_without_tests) > 0:
        print('warning: the following modules have no tests configured:')
        for module in sorted(modules_without_tests):
            print('  ', module)
    successful_test_count = print_test_group(
        'The following {} tests succeeded:', 
        TestResult.success)
    missing_test_count = print_test_group(
        'The following {} tests are missing (build failed?):', 
        TestResult.notrun)
    failed_test_count = print_test_group(
        'The following {} tests failed:', 
        TestResult.fail)
    if missing_test_count > 0 or failed_test_count > 0:
        raise Exception('ERROR: {} tests failed and {} tests failed building'\
                        .format(failed_test_count, missing_test_count))
    print('All {} tests successful.'.format(successful_test_count))

def cmd_make():
    """ this command makes some educated guesses about which toolchain
        the user probably wants to run, then invokes gyp to create the
        makefiles for this toolchain and invokes the build. On Linux
        'bru make' is likely equivalent to:
           >gyp *gyp --depth=.
           >make
        On Windows it's likely equivalent to:
           >gyp --depth=. package.gyp -G msvs_version=2012
           >C:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild.exe package.sln
        The main purpose of 'bru make' is really to spit out these two
        command lines as a quick reminder for how to build via cmd line.
    """

    # first locate the single gyp in the cwd
    bru_file = brulib.install.get_single_bru_file('.')
    if bru_file == None:
        raise Exception("there's no *.bru file in current work dir, "
            'e.g. run "bru install googlemock" first to create one')
    gyp_file = bru_file[:-3] + 'gyp'
    if not os.path.exists(gyp_file):
        raise Exception(bru_file,'has no companion *.gyp file, '
            'e.g. recreate one via "bru install googlemock"')

    system = platform.system()
    if system == 'Windows':
        cmd_make_win(gyp_file)
    elif system == 'Linux':
        cmd_make_linux(gyp_file)
    else:
        raise Exception('no idea how to invoke gyp & toolchain on platform {}'\
            .format(system))

def get_latest_msbuild_exe():
    """ return path to latest msbuild on Windows machine """
    env = os.environ
    windir = env['SystemRoot'] if 'SystemRoot' in env else env['windir']
    glob_expr = os.path.join(windir, 'Microsoft.NET', 'Framework',
        '**', 'msbuild.exe')
    msbuilds = glob.glob(glob_expr)
    return max(msbuilds)  # not alphanumeric, should be good enough tho

def get_latest_msvs_version():
    """ e.g. return 2012 (aka VC11) if msvs 2012 is installed. If multiple
        vs versions are installed then pick latest.
        Return None if no installs are found?
    """
    # whats a good way to detect the msvs version?
    # a) scan for install dirs like
    #    c:\Program Files (x86)\Microsoft Visual Studio 10.0
    # b) scan for env vars like VS110COMNTOOLS
    # Let's do (b) for now.
    # See also https://code.google.com/p/gyp/source/browse/trunk/pylib/gyp/MSVSVersion.py
    msvs_versions = []
    regex = re.compile('^VS([0-10]+)COMNTOOLS$')
    for key in os.environ:
        match = regex.match(key)
        if match != None:
            msvs_versions.append(int(match.group(1)))
    if len(msvs_versions) == 0:
        return None
    latest = max(msvs_versions) # e.g. 110
    if len(msvs_versions) > 1:
        print('detected installs of msvs {}, choosing latest {}'.format(
            msvs_versions, latest))
    msvs_version2year = {
        80: 2005,
        90: 2008,
        100: 2010,
        110: 2012,
    }
    if not latest in msvs_version2year:
        print('not sure how to map VC{} to a VS year, defaulting to VS 2012'
            .format(latest))
        return 2012
    return msvs_version2year[latest]

def run_gyp(gyp_cmdline):
    print('running >', gyp_cmdline)
    returncode = os.system(gyp_cmdline)
    if returncode != 0:
        raise Exception('error running gyp, did you install it?'
            ' Instructions at https://github.com/KjellSchubert/bru')

def cmd_make_win(gyp_filename):
    # TODO: locate msvs version via glob
    msvs_version = get_latest_msvs_version()
    if msvs_version == None:
        print('WARNING: no msvs installation detected, did you install it? '
            'Defaulting to msvs 2012.')
    gyp_cmdline = 'gyp --depth=. {} -G msvs_version={}'.format(
        gyp_filename, msvs_version)
    run_gyp(gyp_cmdline)
    # gyp should have created a *.sln file, verify that.
    # if it didnt that pass a msvc generator option to gyp in a more explicit
    # fashion (is -G msvs_version enough? need GYP_GENERATORS=msvs?).
    sln_filename = gyp_filename[:-3] + 'sln'
    if not os.path.exists(sln_filename):
        raise Exception('gyp unexpectedly did not generate a *.sln file, '
            'you may wanna invoke gyp manually to generate the expected '
            'make/sln/ninja files, e.g. set GYP_GENERATORS=msvs')

    # there are many ways to build the *.sln now, e.g. pass it to devenv
    # or alternatively to msbuild. Lets do msbuild here:
    # TODO locate msbuild via glob
    msbuild_exe = get_latest_msbuild_exe()
    if msbuild_exe == None:
        raise Exception('did not detect any installs of msbuild, these should'
            ' be part of .NET installations, please install msbuild or .NET')
    config = 'Release'
    msbuild_cmdline = '{} {} /p:Configuration={}'.format(
        msbuild_exe, sln_filename, config)
    print('running msvs via msbuild >', msbuild_cmdline)
    returncode = os.system(msbuild_cmdline)
    if returncode != 0:
        raise Exception('msbuild failed with errors, returncode =', returncode)
    print('Build complete.')

def cmd_make_linux(gyp_filename):
    # Here we could check if ninja or some such is installed to generate ninja
    # project files. But for simplicity's sake let's just use whatever gyp
    # defaults to.

    # For some odd reason passing './package.gyp' as a param to gyp will 
    # generate garbage, instead you gotta pass 'package.gyp'. Se let's 
    # explicitly remove a leading ./
    dirname = os.path.dirname(gyp_filename)
    assert dirname == '.' or len(dirname) == 0
    gyp_filename = os.path.basename(gyp_filename)
    
    gyp_cmdline = 'gyp --depth=. {}'.format(gyp_filename)
    run_gyp(gyp_cmdline)
    if not os.path.exists('Makefile'):
        raise Exception('gyp did not generate ./Makefile, no idea how to '
            'build with your toolchain, please build manually')
    returncode = os.system('make')
    if returncode != 0:
        raise Exception('Build failed: make returned', returncode)
    print('Build complete.')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_install = subparsers.add_parser('install')
    parser_install.add_argument("installables", default = [], nargs = '*',
                                help = 'e.g. googlemock@1.7.0')

    parser_test = subparsers.add_parser('test')
    parser_test.add_argument("testables", default = [], nargs = '*',
                                help = 'e.g. googlemock')

    parser_test = subparsers.add_parser('make')

    args = parser.parse_args()
    library = get_library()
    if args.command == 'install':
        brulib.install.cmd_install(library, args.installables)
    elif args.command == 'make':
        cmd_make()
    elif args.command == 'test':
        cmd_test(args.testables)
    else:
        raise Exception("unknown command {}, chose install | test".format(args.command))

if __name__ == "__main__":
    main()
