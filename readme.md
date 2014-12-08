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
