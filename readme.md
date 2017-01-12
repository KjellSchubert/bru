This here is experimental work in progress.

[![Build Status](https://travis-ci.org/KjellSchubert/bru.svg?branch=master)](https://travis-ci.org/KjellSchubert/bru)
[![Coverage Status](https://coveralls.io/repos/KjellSchubert/bru/badge.png)](https://coveralls.io/r/KjellSchubert/bru)


Goal: download common open-source C++ dependencies like ICU, boost-regex, 
cryptopp in a similar way as other package managers do that in other languages,
e.g. npm for nodejs, pip for python and so on. This process here is supposed 
to replace our current labor-intensive way of upgrading 3rd party OSS 
dependencies to new versions of the dependencies themselves or the toolchains
using them: this current process requires a painful manual sequence of wget, 
optional patch & configure, build, apache-ivy publish to Artifactory, and
updating Ivy files for each combination of toolchain & library. Which makes
toolchain upgrades less fun than they should be :)

Usage example:
```
>bru install googlemock
created foo\package.bru
added dependency googlemock@1.7.0 to foo\package.bru and foo\package.gyp
processing dependency googlemock version 1.7.0 requested by foo\package.bru
unpacking C:\Users\<me>\.bru\downloads\googlemock\1.7.0\files_gmock-1.7.0.zip
processing dependency googletest version 1.7.0 requested by googlemock
unpacking C:\Users\<me>\.bru\downloads\googletest\1.7.0\files_gtest-1.7.0.zip
copying bru_common.gypi
creating empty bru_overrides.gypi

>bru test
executable for googlemock:googlemock_test not found
running 'bru make --config Debug --targetPlatform Native'
running 'gyp --depth=. .\package.gyp -G msvs_version=2012'
running msvs via msbuild: 'C:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild.exe .\package.sln /p:Configuration=Debug /verbosity:minimal'
...
Build complete.
running googlemock_test
...
The following 2 tests succeeded:
  googlemock:googlemock_test after 119 ms
  googletest:googletest_sample1 after 46 ms
All 2 tests successful.
```

Existing projects like
[Homebrew](http://brew.sh/) already download & build Boost, e.g. see 
[here](https://github.com/Homebrew/homebrew/blob/master/Library/Formula/boost.rb).
Why not just use Homebrew? Homebrew appears to be MacOS-specific. Besides 
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
* should build upstream modules in-place, there's no requirement for sharing 
  binaries of upstream modules to reduce the number of local builds. Initially
  I had planned to share binaries, but this would be a lot of effort for
  questionable value. Compiler ABI compatibilty and dependencies on
  different std libs are complex topics.
* is supposed to deal with multiple C++ standard libs gracefully: e.g. if one
  project happens to use Clang 3.5 with GCC 4.9's C++ standard library and 
  another uses an incompatible standard lib like http://libcxx.llvm.org/ or
  Dinkumware or STLPort then conflicts must be resolved. 
  This is not much different from resolving e.g. Boost version conflicts in
  different dependencies, except often people aren't even aware of which 
  stdlib they are using.
* is supposed to be able to optionally run tests of upstream dependencies to
  get some confidence that a dependency works as advertised.
* should use existing cross-platform build tools like [CMake](http://www.cmake.org/)
  or Chromium's [gyp](https://code.google.com/p/gyp/) or
  [gn](https://code.google.com/p/chromium/wiki/gn) or hilarious 
  [tup](http://gittup.org/tup/) as much as possible. 
  Of these I ended up depending on gyp.
* should specify dependencies similar as nodejs:npm's package.json or 
  python:pip's requirements.txt
* the tool should be easy to install, e.g. 'python3:pip install bru' would be
  desirable, especially since build tools like gyp already depend on Python(2).
  Atm installations consists of a 'git clone', update via 'git pull'.
* support debug vs release builds
* needs to deal with msvs's /MT vs /MD, static vs dynamic CRT builds
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

```
sudo apt-get install python  # Python 2.x, usually preinstalled
sudo apt-get install python3
```

Verify Python install:

```
python --version # should print 2.x
python3 --version # should print 3.x
```

Install gyp:

```
sudo apt-get install gyp
```


Installing prerequisites on Windows
---

Install Python 2.x (needed for gyp) and Python 3.x (needed for bru) the usual
way: 

```
choco install python2
choco install python3
```

Sadly the current chocolatey Python 3.4.2 install does not create a python3
symlink yet, so do that manually:

```
cd c:\tools\python3
ln python.exe python3.exe
ln Scripts\pip3.exe pip3.exe
```

As of December 2014 'choco install python2' does not add c:\tools\python2\Scripts
to your PATH so do that manually now, using the equivalent of:

```
set PATH=%PATH%;c:\tools\python2\Scripts
```

Verify Python install:

```
python --version # should print 2.x
python3 --version # should print 3.x
pip2 --version
pip3 --version
```

Install gyp: chocolatey.org does not have gyp available as of Dec 2014,
(searching for gyp yields ninja only) and it's not available from pypi either,
so install latest gyp from source:

```
choco install svn # unless you have svn installed already
svn checkout http://gyp.googlecode.com/svn/trunk/ gyp-read-only 
cd gyp-read-only; python setup.py install
```

Verify that the 'gyp' command works outside the gyp-read-only dir:

```
cd ..
gyp -h
```

If this doesn't work check [here](https://code.google.com/p/gyp/issues/detail?id=170) 
for a potential solution (is copying the gyp.bat file still necessary?) and make sure
gyp.exe or gyp.bat are in your path (via c:\tools\python2\Scripts).

See [here](https://github.com/KjellSchubert/bru-sample) for how to build a small
sample application using bru.

Installing bru itself
===

On Ubuntu:
---

```
cd ~
git clone https://github.com/KjellSchubert/bru.git
sudo ln `pwd`/bru/bru.sh /usr/bin/bru
```

On Windows:
---

```
cd c:\tools # this is where choco installs many apps like python for example
git clone https://github.com/KjellSchubert/bru.git
set PATH=%PATH%;c:\tools\bru # to make bru[.bat] accessible from anywhere
```