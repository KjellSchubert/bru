This here is experimental work in progress.

Goal: download common open-source C++ dependencies like ICU, boost-regex, 
cryptopp in a similar way as other package managers do that in other languages,
e.g. npm for nodejs, pip for python and so on. This process here is supposed 
to replace our current labor-intensive way of upgrading 3rd party OSS 
dependencies to new versions of the dependencies themselves or the toolchains
using them: this current process requires a painful manual sequence of wget, 
optional patch & configure, build, apache-ivy publish to Artifactory, and
updating Ivy files for each combination of toolchain & library. Which makes
toolchain upgrades less fun than they should be :)

Existing projects like
[Homebrew](http://brew.sh/) already download & build Boost, e.g. see 
[here](https://github.com/Homebrew/homebrew/blob/master/Library/Formula/boost.rb).
Why not just use Homebrew? Homebrew appears to be MacOS-specific. Besides Homebrew
since Homebrew seems to be more like apt-get/yum than npm it doesn't seem to be
dealing with different versions of products, e.g. atm it
always downloads Boost 1.56, so downstream projects that for whatever reason
require Boost 1.49 would be forced to upgrade to a newer incompatible version.

Are there other C++ dependency managers that do more or less the same thing? I
don't think so, I've seen a few dead projects though, so good luck to this one 
here. Similar projects:

* semi-dead https://github.com/iauns/cpm
* semi-dead [nuget: GoingNative 2013](http://channel9.msdn.com/Events/GoingNative/2013/Find-Build-Share-Use-Using-NuGet-for-C-and-Cpp-Libraries)
* [node-gyp](https://github.com/TooTallNate/node-gyp) can build native libs for
  nodejs's npm package manager. Not sure if this can deal with pulling 
  dependency chains of C++ libs, probably not easily. There are bindings for
  several C++ projects on npmjs.org/, e.g. https://www.npmjs.org/package/cryptopp 
  or https://www.npmjs.org/package/node-icu-charset-detector.
* travis.ci skips dependency downloads for C++ projects, but you can inject
  a shell script that pulls deps, see 
  [here](http://docs.travis-ci.com/user/languages/cpp/)
* in beta stage, looks very promising: [biicode](https://www.biicode.com)
* work in progress?: 
  [C++ builds with Gradle](http://www.gradleware.com/video/creating-a-world-class-cc-build-system-in-gradle-2/),
  see also blog entry [here](http://blog.biicode.com/file-based-cpp-dependency-manager/). 
  At this point biicode lacks many of the deps we need, and it's not clear to
  me how to get our deps in there.

Requirements:

* is supposed to work cross-platform on at least Linux, Windows, MacOS
* is supposed to be able to download & build different versions of dependencies 
  like Boost & resolve conflicts if different downstream dependencies ask for 
  different versions of Boost.
* is supposed to be able to store successful builds of dependencies in a 
  hierarchy of caches, e.g. in the user's home directory, and optionally in an
  organization-internal cache (e.g. a simple webserver that can deal with HTTP 
  GET and PUT of boost-v110-s.lib.gz and boost-includes.tar.gz). That allows
  developers in the organization to fetch upstream OSS dependencies without
  having to rebuild them locally. Besides that it allows a single developer to
  use e.g. cryptopp 1.99 in multiple C++ projects without having to rebuild it
  individually for each.
* is supposed to deal with multiple C++ standard libs gracefully: e.g. if one
  project happens to use Clang 3.5 with GCC 4.9's C++ standard library and 
  another uses an incompatible standard lib like http://libcxx.llvm.org/ or
  Dinkumware or STLPort then conflicts must be resolved. 
  This is not much different from resolving e.g. Boost version conflicts in
  different dependencies, except often people aren't even aware of which 
  stdlib they are using.
* is supposed to deal with compilation of dependencies for different C++ 
  standards: if one project needs boost 1.56 compiled for a C++98 project and 
  and another for C++14 then different Boost libs need to be downloaded for each.
* is supposed to deal with different & ABI-incompatible toolchains on the same
  machine: e.g. if a machine has installed an old ICC and a recent Clang that
  happen to be ABI-incompatible then different Boost libs need to be downloaded 
  for each.
* is supposed to be able to optionally run tests of upstream dependencies to
  get some confidence that a downloaded or just built dependency works as 
  advertised.
* should use existing cross-platform build tools like [CMake](http://www.cmake.org/)
  or Chromium's [gyp](https://code.google.com/p/gyp/) or
  [gn](https://code.google.com/p/chromium/wiki/gn) or hilarious 
  [tup](http://gittup.org/tup/) as much as possible.
* should specify dependencies similar as nodejs:npm's package.json or 
  python:pip's requirements.txt
* should rather generate compiler or linker errors than silent ODR violations with
  crashes at runtime
* the tool should be easy to install, e.g. 'python3:pip install bru' would be
  desirable, especially since build tools like gyp already depend on Python(2).
* do we want support for debug vs release builds? Probably.
* do we want support for /MT vs /MD, static vs dynamic lib builds? Yes.
* do we want support for project-specific configurations beyond debug/release?
  Probably. E.g. for SSE2 vs non-SSE builds.
* do we want support for different OS versions? Some Windows libraries do
  things like #if WINVER > 0x400, see 
  [here](http://blogs.msdn.com/b/oldnewthing/archive/2007/04/11/2079137.aspx).
  Note that this identifies the (minimum) target OS for cross-compilation, not 
  the compiler's host OS. So depending on what you set WINVER to during compilation
  you can end up with different binaries with different functionality.

Example for what the tool does:

1. read package.json-equivalent to determine upstream dependencies
2. download recipes for these deps, which includes their recursive deps as well
   as build instruction similar to 
   https://github.com/Homebrew/homebrew/blob/master/Library/Formula/boost.rb
3. resolve conflicts between upstream dependencies (e.g. if 2 deps want
   to depend on different versions of Boost). Conflicts obviously can easily
   lead to compiler errors in one of the dependencies that's forced on a 
   different version of Boost.
4. download resolved dependencies (includes and libs) from ~/.bru or
   https://local-artifactory.blabla.org if possible
5. build dependencies that couldnt be downloaded, publish them to the cache
   after successful builds & tests (shared caches will require some amount of trust
   between users of the cache to not push backdoor-infused libs)
6. end up with (usually) downloaded & (sometimes) locally built dependencies
   in ./bru_modules, similar to how npm populates ./node_modules

The user can then use whatever local build tool he prefers (*.vcproj, *.gyp, 
*.make, ...), referring to the downloaded/built includes & libs of 3rd party
dependencies in ./bru_modules.

Installing prerequisites
===

Installing prerequisites on Ubuntu
---

Install Python 2.x (needed for gyp) Python 3.x (needed for bru) the usual way:

>sudo apt-get install python  # Python 2.x, usually preinstalled
>sudo apt-get install python3

Verify Python install:

>python --version # should print 2.x
>python3 --version # should print 3.x

Install gyp:

>sudo apt-get install gyp


Installing prerequisites on Windows
---

Install Python 2.x (needed for gyp) and Python 3.x (needed for bru) the usual
way: 

>choco install python2
>choco install python3

Sadly the current chocolatey Python 3.4.2 install does not create a python3
symlink yet, so do that manually:

>cd c:\tools\python3
>ln python.exe python3.exe
>ln Scripts\pip3.exe pip3.exe

As of December 2014 'choco install python2' does not add c:\tools\python2\Scripts
to your PATH so do that manually now, using the equivalent of:

>set PATH=%PATH%;c:\tools\python2\Scripts

Verify Python install:

>python --version # should print 2.x
>python3 --version # should print 3.x
>pip2 --version
>pip3 --version

Install gyp: chocolatey.org does not have gyp available as of Dec 2014,
(searching for gyp yields ninja only) and it's not available from pypi either,
so install latest gyp from source:

>choco install svn # unless you have svn installed already
>svn checkout http://gyp.googlecode.com/svn/trunk/ gyp-read-only 
    (as described [here](https://code.google.com/p/gyp/issues/detail?id=170))
>cd gyp-read-only; python setup.py install # note that's python 2.x

Verify that the 'gyp' command works outside the gyp-read-only dir:

>cd ..
>gyp -h

If this doesn't work check [here](https://code.google.com/p/gyp/issues/detail?id=170) 
for a potential solution (is copying the gyp.bat file still necessary?) and make sure
gyp.exe or gyp.bat are in your path (via c:\tools\python2\Scripts).


Building the test application
===

The same steps should work on both Windows & Ubuntu with only few differences:

>git clone https://github.com/KjellSchubert/bru.git
>cd bru
>python3 bru.py install foo.bru # TODO: syntax will likely change
>gyp --depth=. foo.gyp # TODO: avoid the --depth=.

On Ubuntu this will generate makefiles for make, and on Windows vcxproj files for 
VisualStudio 2010 (or whatever VS you have installed?). To generate project files 
for other build systems like ninja or VS2012 for example run gyp with a different 
generator:

Building the test application on Ubuntu
---

Generate a Makefile for make:

>gyp --depth=. foo.gyp

To build via make:

>make

To run the generated executables:

>out/Default/foo-test
>out/Default/googletest_sample1

Building the test application on Windows
---

Generate vcproj files for VS2012 (assuming that's the VS version you have 
installed):

>gyp --depth=. foo.gyp -G msvs_version=2012

Now open ./foo.sln in VS2012 and build the solution, or alternatively build with 
msbuild via command line:

>C:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild.exe foo.sln

Then run the generated executables:

>Default\foo-test.exe
>Default\googletest_sample1.exe

Note that many of the VS compiler & linker settings get defaults via
common.gypi in the root of your project. This common.gypi is included
by the gyp files of the individual modules, e.g. see 
bru_modules\googletest\googletest.gyp with its "includes" directive.

