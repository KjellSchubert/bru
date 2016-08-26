""" this module impls the logic for 'bru test' """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import glob
import time
import subprocess
import itertools
import brulib.jsonc
import brulib.make

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

# initially this was an (3.4) Enum, but I reduced the requirement to 3.2, see
# .travis.yml for details.
# So this here simulates a Python Enum:
class TestResult:
    pass
TestResult.fail = 0
TestResult.success = 1
TestResult.notrun = 2 # e.g. not run because executable wasnt built or wasnt found

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
            os.path.join('lib', config, target_name),
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
        # build Debug config, it compiles faster
        verbose = 0
        brulib.make.cmd_make('Debug', verbose)

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
