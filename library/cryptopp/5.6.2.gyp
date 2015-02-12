{
    "targets": [
        {
            "target_name": "cryptopp",
            "type": "static_library",

            # WARNING: since cryptopp doesn't put its include files into a
            # subdir, and since it has many dangerous short #include file names
            # (like cpu.h) you end up with code like:
            #   #include "3des.h"
            # in your client code. This is also how cryptopp example code
            # includes its files. This effectively risks shadowing #include
            # files from other libs that do the same thing (e.g. zlib), so
            # good luck using cryptopp in large projects :)
            "include_dirs": [
                "5.6.2"
            ],

            "sources": [
                "5.6.2/*.cpp"
            ],
            "sources!": [
                # I wish I could simply specify "5.6.2/*.cpp" above, but
                # crpytopp tosses test and source files into the same dir.
                # Its GNUMakefile uses this expression:
                #   TESTOBJS = bench.o bench2.o test.o validat1.o ... dlltest.o
                #   LIBOBJS = $(filter-out $(TESTOBJS),$(OBJS))
                # So excluding the list of test files here (TODO: dont have
                # 2 copies of the same list around)
                "5.6.2/bench.cpp",
                "5.6.2/bench2.cpp",
                "5.6.2/datatest.cpp",
                "5.6.2/dlltest.cpp",
                "5.6.2/regtest.cpp",
                "5.6.2/test.cpp",
                "5.6.2/validat1.cpp",
                "5.6.2/validat2.cpp",
                "5.6.2/validat3.cpp",
                "5.6.2/fipsalgt.cpp"
            ],

            # TODO: add msvs pch.h support if possible

            "conditions": [
                ["OS=='win'", {
                    "link_settings" : {
                        "libraries" : [
                            "-lws2_32.lib" # really? socket lib? Link err otherwise
                        ]
                    }
                }],
                ["OS=='mac'", { 
                    "defines": [
                        "CRYPTOPP_DISABLE_ASM"
                    ]

                }],
                ["OS=='iOS'", { 
                    "defines": [
                        "CRYPTOPP_DISABLE_ASM"
                    ]

                }],
                ["OS=='linux'", { # TODO: only for compilation with clang?

                    # WARNING: I ran into these issues here with clang 3.4 on Centos:
                    #   http://permalink.gmane.org/gmane.comp.encryption.cryptopp/6853
                    #   https://groups.google.com/forum/#!topic/cryptopp-users/OWaVmOH6oFY
                    # getting these GNU_ASL errors. Setting env var AS didn't work for
                    # me, so disabling asm for now for this module, which will likely
                    # make the benchmark slower. Only need this module for some legacy
                    # code, so have no incentive to find a faster/better solution.
                    # P.S.: gcc 4.8 doesn't understand this flag, not sure how to make
                    # it conditional most easily. I'm adding -no-integrated-as as
                    # a global option to bru_overrides.gypi for now.
                    #"cflags": [
                    #    "-no-integrated-as"
                    #],
                    # P.S. this problem showed up again for me on Ubuntu 14 with 
                    # clang 3.5. Trying solution from http://braumeister.org/formula/cryptopp,
                    # so no need for cflags -no-integrated-as any more.
                    "defines": [
                        "CRYPTOPP_DISABLE_ASM"
                    ]

                }]
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "5.6.2"
                ]
            }

        },

        # 'cryptest v' runs a sort-of-quick set of tests: it's quick in
        # release builds with asm enabled, but 1 min if you enable clangs
        # address sanitizer and disable asm.
        {
            "target_name": "cryptest",
            "type": "executable",

            # this single test executable bundles a lot of tests and tools:
            #   * v runs a 1min unit test suite: valuable, but slow
		    #   * b runs benchmarks, even slower
            # I couldn't find a faster test, so tempted to disable this for now.
            "test": {
                "cwd": "5.6.2",
                "args": [ "v" ]
            },
            "sources": [
                "5.6.2/bench.cpp",
                "5.6.2/bench2.cpp",
                "5.6.2/datatest.cpp",
                "5.6.2/dlltest.cpp",
                "5.6.2/regtest.cpp",
                "5.6.2/test.cpp",
                "5.6.2/validat1.cpp",
                "5.6.2/validat2.cpp",
                "5.6.2/validat3.cpp",
                "5.6.2/fipsalgt.cpp"
            ],
            "dependencies": [
                "cryptopp"
            ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        }
    ]
}
