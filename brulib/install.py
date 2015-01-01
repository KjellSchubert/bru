""" this here's the code responsible for executing 'bru install' commands, e.g.
    'bru install package.json' or 'bru install protobug googlemock@1.7.0'.
"""

import os
import re
import glob
import shutil
import filecmp
import platform
import collections
import brulib.jsonc
import brulib.module_downloader

class Installable:
    def __init__(self, module, version):
        self.module = module
        self.version = version
        
    def __eq__(self, other):
        if not isinstance(other, Installable):
            return False
        return self.module == other.module and self.version == other.version
        
def get_single_bru_file(dir):
    """ return None of no *.bru file in this dir """
    matches = glob.glob(os.path.join(dir, "*.bru"))
    if len(matches) == 0:
        return None
    if len(matches) > 1:
        raise Exception("there are multiple *.bru files in {}: {}".format(
              dir, matches))
    return matches[0]

def get_or_create_single_bru_file(dir):
    """ returns single *.bru file from given dir or creates an empty
        package.bru file (corresponding to package.json for npm).
        So unlike get_single_bru_file() never returns None.
    """
    bru_file = get_single_bru_file(dir)
    if bru_file == None:
        bru_file = os.path.join(dir, 'package.bru')
        brulib.jsonc.savefile(bru_file, {'dependencies':{}})
        print('created ', bru_file)
    assert bru_file != None
    return bru_file

def parse_module_at_version(installable):
    """ parses 'googlemock@1.7.0' into tuple (module, version),
        and returns (module, None) for input lacking the @version suffix.
    """
    elems = installable.split('@')
    if len(elems) == 1:
        return Installable(elems[0], None)
    if len(elems) == 2:
        return Installable(elems[0], elems[1])
    raise Exception("expected module@version but got {}".format(installable))

def parse_existing_module_at_version(installable, library):
    """ like parse_module_at_version but returns the latest version if version
        was unspecified. Also verifies module at version actually exist
        in ./library.
        Param library is of type brulib.library.Library
    """
    installable = parse_module_at_version(installable)
    module = installable.module
    version = installable.version
    if not os.path.exists(library.get_module_dir(module)):
        raise Exception("no module {} in {}, may want to 'git pull'"\
              " if this module was added very recently".format(
              module, library.get_root_dir()))
    if version == None:
        version = library.get_latest_version_of(module)
    if not library.has_formula(module, version):
        raise Exception("no version {} in {}/{}, may want to 'git pull'"\
              " if this version was added very recently".format(
              version, library.get_root_dir(), module))
    assert version != None
    return Installable(module, version)

def add_dependencies_to_bru(bru_filename, installables):
    bru = brulib.jsonc.loadfile(bru_filename)
    if not 'dependencies' in bru:
        bru['dependencies'] = {}
    deps = bru['dependencies']
    for installable in installables:
        deps[installable.module] = installable.version
    brulib.jsonc.savefile(bru_filename, bru) # warning: this nukes comments atm

def add_dependencies_to_gyp(gyp_filename, installables):
    gyp = brulib.jsonc.loadfile(gyp_filename)
    # typically a gyp file has multiple targets, e.g. a static_library and
    # one or more test executables. Here we add the new dep to only the first
    # target in the gyp file, which is somewhat arbitrary. TODO: revise.
    # Until then end user can always shuffle around dependencies as needed
    # between targets.
    if not 'targets' in gyp:
        gyp['targets'] = []
    targets = gyp['targets']
    if len(targets) == 0:
        targets[0] = {}
    first_target = targets[0]
    if not 'dependencies' in first_target:
        first_target['dependencies'] = []
    deps = first_target['dependencies']
    for installable in installables:
        module = installable.module
        dep_gyp_path = "bru_modules/{}/{}.gyp".format(module, module)
        dep_expr = dep_gyp_path + ":*" # depend on all targets, incl tests
        if not dep_expr in deps:
            deps.append(dep_expr)
    brulib.jsonc.savefile(gyp_filename, gyp) # warning: this nukes comments atm

def create_gyp_file(gyp_filename):
    """ creates enough of a gyp file so that we can record dependencies """
    if os.path.exists(gyp_filename):
        raise Exception('{} already exists'.format(gyp_filename))
    gyp = collections.OrderedDict([
        ("includes", [
            # bru_common.gypi should in general not be edited, but stay a copy
            # of the original. If you want to override settings in this gypi
            # file then you're better off editing bru_overrides.gypi.
            # That way if bru_common.gyp gets improvements in git you don't 
            # need to merge these external changes with your local ones.
            "bru_common.gypi",
            # This is the gypi file you're encourage to edit, bru will always
            # keep this empty and untouched.
            "bru_overrides.gypi"
        ]),
        ("targets", [
            collections.OrderedDict([
                ("target_name", "foo"), # just a guess, user should rename
                ("type", "none"), # more likely 'static_library' or 'executable'

                # these two props are going to have to be filled in by enduser
                ("sources", []),
                ("includes_dirs", []),

                ("dependencies", [])
        ])])
    ])
    brulib.jsonc.savefile(gyp_filename, gyp)

# from http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
class Chdir:
    """ Context manager for changing the current working directory.
        Used in conjunction with os.system for executing $make_command,
        typically used to run ./configure
    """
    def __init__( self, newPath ):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def touch(file_name, times=None):
    # http://stackoverflow.com/questions/1158076/implement-touch-using-python
    with open(file_name, 'a'):
        os.utime(file_name, times)

def exec_make_command(formula, bru_modules_root, system):
    """ note that few modules specify a make_command. The few that do usually
        don't execute a full make but only a ./configure.
        This part is kinda ugly atm: consistent use of gyp for building modules
        we depent on would be preferable. TODO: revisit.
        param system should be platform.system()
    """
    # make_command should only be used if we're too lazy to provide a
    # gyp file for a module.
    # A drawback of using ./configure make is that build are less reproducible
    # across machines, e.g. ./configure may enable some code paths on one
    # machine but not another depending on which libs are installed on both
    # machines.
    if 'make_command' in formula:
        module_dir = os.path.join(bru_modules_root, formula['module'], formula['version'])
        make_done_file = os.path.join(module_dir, "make_command.done")
        if not os.path.exists(make_done_file):
            # pick a make command depending on host OS
            make_commands = formula['make_command']
            if not system in make_commands:
                raise Exception("no key {} in make_command".format(system))
            make_command = make_commands[system]
            
            # exec make_command with cwd being the module_dir (so the dir the
            # gyp file is in, not that the gyp file is used here, but using the
            # same base dir for the gyp & make_command probably makes sense)
            with Chdir(module_dir):
                print("building via '{}' ...".format(make_command))
                error_code = os.system(make_command)
                if error_code != 0:
                    raise ValueError("build failed with error code {}".format(error_code))
            touch(make_done_file)

def download_module(library, module_name, module_version):
    bru_modules_root = "./bru_modules"
    formula = library.load_formula(module_name, module_version)
    brulib.module_downloader.get_urls(library, formula, bru_modules_root)
    exec_make_command(formula, bru_modules_root, platform.system())

def verify_resolved_dependencies(formula, target, resolved_dependencies):
    """ param formula is the formula with a bunch of desired(!) dependencies
        which after conflict resolution across the whole set of diverse deps
        may be required to pull a different version for that module for not
        violate the ODR. But which of course risks not compiling the module
        (but which hopefully will compile & pass tests anyway).
        Param resolved_dependencies is this global modulename-to-version map
        computed across the whole bru.json dependency list.
        Returns the subset of deps for the formula, using the resolved_dependencies
    """

    # this here's the module we want to resolve deps for now:
    module = formula['module']
    version = formula['version']

    # iterate over all target and their deps, fill in resolved versions
    target_name = target['target_name']
    resolved_target_deps = []

    def map_dependency(dep):
        """ param dep is a gyp file dependency, so either a local dep to a local
            target like 'zlib' or a cross-module dep like '../boost-regex/...'.
            There should be no other kinds of gyp deps in use """

        # detect the regexes as written by scan_deps.py: references into
        # a sibling module within ./bru_modules.
        bru_regex = "^../([^/]+)/([^/]+)\\.gyp:(.+)"
        match = re.match(bru_regex, dep)
        if match == None:
            return dep
        upstream_module = match.group(1)
        upstream_targets = match.group(2)
        if not upstream_module in resolved_dependencies:
            raise Exception("module {} listed in {}/{}.gyp's target '{}'"
                " not found. Add it to {}/{}.bru:dependencies"
                .format(
                    upstream_module, module, version, target_name,
                    module, version
                ))
        return resolved_dependencies[upstream_module]
    return list(map(map_dependency, target['dependencies']))

def apply_glob_exprs(formula, sources):
    """ gyp does not support glob expression or wildcards in 'sources', this
        here turns these glob expressions into a list of source files.
        param sources is target['sources'] or target['sources!']
    """
    def is_glob_expr(source):
        return '*' in source
    gyp_target_dir = os.path.join('bru_modules', formula['module']) # that is
        # the dir the gyp file for this module is being stored in, so paths
        # in the gyp file are interpreted relative to that
    result = []
    for source in sources:
        if source.startswith('ant:'):
            raise Exception('Ant-style glob exprs no longer supported: ' + source)
        if is_glob_expr(source):
            matching_sources = [os.path.relpath(filename, start=gyp_target_dir)
                                for filename in
                                glob.glob(os.path.join(gyp_target_dir, source))]
            assert len(matching_sources) > 0, "no matches for glob " + source
            result += matching_sources
        else:
            # source os a flat file name (relative to gyp parent dir)
            result.append(source)
    return list(sorted(result))

def apply_recursive(dic, func):
    """ param dic is usually a dictionary, e.g. 'target' or 'condition' 
              child node. It can also be a child dict or child list of
              these nodes/dicts
        param func is a func to be applied to each child dictionary, taking
              the dictionary as the only param
    """
    if isinstance(dic, dict):
        func(dic)
        for key, val in dic.items():
            if isinstance(val, dict) or isinstance(val, list):
                apply_recursive(val, func)
    if isinstance(dic, list):
        for elem in dic:
            apply_recursive(elem, func)

def apply_glob_to_sources(dic, formula):
    """ param dic is a 'target' dictionary, or one of the childnodes
        in a 'conditions' list
    """
    for prop in ['sources', 'sources!']:
        if prop in dic:
            dic[prop] = apply_glob_exprs(formula, dic[prop])

def copy_gyp(library, formula, resolved_dependencies):
    """
        Param resolved_dependencies is a superset of the deps in formula
        with recursively resolved module versions (after resolving conflicts).
    """

    # If the module has a gyp file then let's copy it into ./bru_modules/$module,
    # so next to the unpacked tar.gz, which is where the gyp file's relative
    # paths expect include_dirs and source files and such.
    # Not all modules need a gyp file, but a gyp file allows specifying upstream
    # module dependencies, whereas a ./configure; make might have easily overlooked
    # dependencies that result in harder-to-reproduce builds (unless you build
    # on only one single machine in your organization).
    # Actually even for modules build via make_command we need a gyp file to
    # specify include paths and module libs via all|direct_dependent_settings.
    #
    # Note that the gyp file in the ./library does not contain 'dependencies'
    # property yet, we add this property now (to not have the same redundant deps
    # both in *.bru and *.gyp in the ./library dir)
    module_name = formula['module']
    assert module_name in resolved_dependencies
    resolved_version = resolved_dependencies[module_name]
    gyp = library.load_gyp(formula)
    for target in gyp['targets']:

        if 'dependencies' in target:
            # Initially I thought there should be no such prop in the
            # library/.../*.gyp file because these deps will be filled in with
            # resolved deps from the *.bru file. But then I ran into two
            # problems:
            #   a) I wanted for example zlib tests to build via gyp also
            #      (espcially since zlib is being built via gyp target alrdy
            #      anyway), so the gyp test target should depend on the lib
            #      target.
            #   b) often test targets need to pull in additional module deps
            #      that the module (without its tests) does not depend on, for
            #      example tests often depend on googletest or googlemock,
            #      whereas the main module does not.
            # So now a *.bru file lists the union of dependencies for all
            # targets in a gyp file, while each target depends explicitly
            # lists dependencies as "bru:googletest". Could also support a
            # format like "bru:googletest:1.7.0" but then the *.gyp file
            # and *.bru file dependency lists would be redundant. Todo: move
            # dependency lists from *.bru to *.gyp file altogether? Maybe...
            verify_resolved_dependencies(formula, target, resolved_dependencies)

        # Sanity check: verify the 'sources' prop doesn't contain glob exprs
        # or wildcards: initially I though gyp was ok with
        #    "sources" : ".../src/*.cc"
        # in *.gyp files because at first glance this 'compiled', but it
        # turned out gyp just silently compiled zero source files in that case.
        #
        # Alternatively we could expand these wildcards now, drawback of that
        # is that the files in ./library are not really *.gyp files anymore,
        # and should probably be called *.gyp.in or *.gyp-bru or something
        # like that.
        # Apply the same mapping to 'sources' in the 'target' itelf and within
        # its childnodes like 'conditions':
        apply_recursive(target, lambda dic: apply_glob_to_sources(dic, formula))


    # note that library/boost-regex/1.57.0.gyp is being copied to
    # bru_modules/boost-regex/boost-regex.gyp here (with some minor
    # transformations that were applied, e.g. expanding wildcards)
    gyp_target_file = os.path.join('bru_modules', module_name, module_name + ".gyp")

    # We also need a certain set of MSVC options imported into gyp files
    # and don't want to repeat the same boring MSVC settings in every single
    # module's individual gyp file. So add common.gypi include unless
    # the module's gyp file explicitly specifies includes already.
    if not 'includes' in gyp:
        # we want the 'includes' at the begin, to achieve this order see
        # http://stackoverflow.com/questions/16664874/how-can-i-add-the-element-at-the-top-of-ordereddict-in-python
        new_gyp = collections.OrderedDict()
        new_gyp['includes'] = [
                '../../bru_common.gypi',
                '../../bru_overrides.gypi'
        ]
        for key, value in gyp.items():
            new_gyp[key] = value
        gyp = new_gyp

    brulib.jsonc.savefile(gyp_target_file, gyp)

    # this file is only saved for human reader's sake atm:
    brulib.jsonc.savefile(os.path.join('bru_modules', module_name, 'bru-version.json'),
        {'version': resolved_version})

def resolve_conflicts(library, dependencies, root_requestor):
    """ takes a dict of modules and version matchers and recursively finds
        all indirect deps. Then resolves version conflicts by picking the newer
        of competing deps, or by picking the version that was requested by the module
        closest to the root of the dependency tree (unsure still).
        param root_requestor is whatever topmost *.bru listed deps, e.g. 'package.bru'
    """
    todo = [(module, version, root_requestor) for (module, version)
            in dependencies.items()]
    recursive_deps = collections.OrderedDict()
    for module_name, version_matcher, requestor in todo:
        module_version = version_matcher # todo: allow for npm-style version specs (e.g. '4.*')
        #print('resolving dependency {} version {} requested by {}'
        #      .format(module_name, module_version, requestor))
        if module_name in recursive_deps:
            resolved = recursive_deps[module_name]
            resolved_version = resolved['version']
            if module_version != resolved_version:
                winning_requestor = resolved['requestor']
                print("WARNING: version conflict for {} requested by first {} and then {}"
                      .format(module_name, winning_requestor, requestor))
                # instead of just letting the 2nd and later requestors loose
                # the competition we could probably do something more sensible.
                # todo?
        else:
            # this is the first time this module was requested, freeze that
            # chosen version:
            formula = library.load_formula(module_name, module_version)
            recursive_deps[module_name] = {
                'version' : module_version,
                'requestor' : requestor
            }

            # then descend deeper into the dependency tree:
            deps = formula['dependencies'] if  'dependencies' in formula else {}
            child_requestor = module_name
            todo += [(child_module, version, child_requestor)
                     for (child_module, version)
                     in deps.items()]

    return [(module, resolved['version'], resolved['requestor'])
            for (module, resolved) in recursive_deps.items()]

def install_from_bru_file(bru_filename, library):
    """ this gets executed when you 'bru install': it looks for a *.bru file
        in cwd and downloads the listed deps """
    package_jso = brulib.jsonc.loadfile(bru_filename)
    recursive_deps = resolve_conflicts(library, package_jso['dependencies'], bru_filename)
    resolved_dependencies = dict((module, version)
        for (module, version, requestor) in recursive_deps)
    for module_name, module_version, requestor in recursive_deps:
        print('processing dependency {} version {} requested by {}'
              .format(module_name, module_version, requestor))
        formula = library.load_formula(module_name, module_version)
        download_module(library, module_name, module_version)
        copy_gyp(library, formula, resolved_dependencies)

    # copy common.gypi which is referenced by module.gyp files and usually
    # also by the parent *.gyp (e.g. bru-sample:foo.gyp).
    # Should end users be allowed to make changes to bru_common.gypi or
    # should they rather edit their own optional bru_overrides.gpyi which 
    # shadowsbru_common.gypi? Let's do the latter. See comments in
    # create_gyp_file for more details.
    # Anyway: just in case the user did make changes to bru_common.gypi 
    # let's only copy it if it's new.
    common_gypi = 'bru_common.gypi'
    overrides_gypi = 'bru_overrides.gypi'
    common_gypi_src = os.path.join(library.get_root_dir(), '..', common_gypi)
    if not os.path.exists(common_gypi):
        print('copying', common_gypi)
        shutil.copyfile(common_gypi_src, common_gypi)
    elif not filecmp.cmp(common_gypi_src, common_gypi):
        print('WARNING: {} differs from {}: it is OK but not recommended'
              ' to modify {}, instead rather modify {}', 
              common_gypi, common_gypi_src, common_gypi, overrides_gypi)

    # create empty bru_overrides.gypi only if it doesn't exist yet
    # One use case for bru_overides.gypi is to tweak the Debug build to
    # include clang -fsanitize=address options.
    if not os.path.exists(overrides_gypi):
        print('creating empty {}'.format(overrides_gypi))
        brulib.jsonc.savefile(overrides_gypi, {})

    #for module, version, requestor in recursive_deps:
    #    for ext in ['bru', 'gyp']:
    #        print("git add -f library/{}/{}.{}".format(module, version, ext))


    # todo: clean up unused module dependencies from /bru_modules?

def cmd_install(library, installables):
    """ param installables: e.g. [] or ['googlemock@1.7.0', 'boost-regex']
        This is supposed to mimic 'npm install' syntax, see
        https://docs.npmjs.com/cli/install. Examples:
          a) bru install googlemock@1.7.0
          b) bru install googlemock
          c) bru install
        Variant (a) is self-explanatory, installing the module of the given
        version. Variant (b) installs the latest known version of the module
        as specified by the versions listed in bru/library/googlemock.
        Variant (c) will install all dependencies listed in the local *.bru
        file (similar as how 'npm install' install all deps from ./package.json).
        Unlike for 'npm install' the option --save is implied, means whatever you
        install will end up in the local *.bru file's "dependencies" list, as
        well as in the companion *.gyp file.
        Param library is of type brulib.library.Library
    """
    if len(installables) == 0:
        # 'bru install'
        bru_filename = get_single_bru_file(os.getcwd())
        if bru_filename == None:
            raise Exception("no file *.bru in cwd")
        print('installing dependencies listed in', bru_filename)
        install_from_bru_file(bru_filename, library)
    else:
        # installables are ['googlemock', 'googlemock@1.7.0']
        # In this case we simply add deps to the *.bru (and *.gyp) file in
        # the cwd and then execute the same as the next 'bru install' would.
        installables = [parse_existing_module_at_version(installable, library)
                        for installable in installables]
        bru_filename = get_or_create_single_bru_file(os.getcwd())
        gyp_filename = bru_filename[:-3] + 'gyp'
        if not os.path.exists(gyp_filename):
            create_gyp_file(gyp_filename)
        add_dependencies_to_bru(bru_filename, installables)
        add_dependencies_to_gyp(gyp_filename, installables)
        for installable in installables:
            print("added dependency {}@{} to {} and {}".format(
                installable.module, installable.version,
                bru_filename, gyp_filename))
        # now download the new dependency just like 'bru install' would do
        # after we added the dep to the bru & gyp file:
        install_from_bru_file(bru_filename, library)
