""" this module impls the logic for 'bru make', which builds the downloaded
   modules via gyp and local compiler toolchain
"""

import os
import platform
import brulib.install

def cmd_make(config):
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
        param config contains 'Release' or 'Debug'
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
        cmd_make_win(gyp_file, config)
    elif system == 'Linux':
        cmd_make_linux(gyp_file, config)
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

def cmd_make_win(gyp_filename, config):
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
    msbuild_cmdline = '{} {} /p:Configuration={}'.format(
        msbuild_exe, sln_filename, config)
    print('running msvs via msbuild >', msbuild_cmdline)
    returncode = os.system(msbuild_cmdline)
    if returncode != 0:
        raise Exception('msbuild failed with errors, returncode =', returncode)
    print('Build complete.')

def cmd_make_linux(gyp_filename, config):
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
    returncode = os.system('make BUILDTYPE={}'.format(config))
    if returncode != 0:
        raise Exception('Build failed: make returned', returncode)
    print('Build complete.')
