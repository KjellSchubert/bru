{
    "targets": [
        {
            # see also http://www.philipreames.com/Blog/2012/06/27/building-facebook-folly/
            # for (outdated?) build instructions.
            "target_name": "folly",
            "type": "static_library",
            "cflags": [ 
                "-std=c++11" # refuses to compile otherwise 
            ],
            "include_dirs": [
                "master/clone/"
            ],
            "sources": [
                "master/clone/folly/wangle/*/*.cpp",
                "master/clone/folly/*.cpp",
                "master/clone/folly/build/*.cpp",
                "master/clone/folly/detail/*.cpp",
                "master/clone/folly/experimental/*.cpp",
                "master/clone/folly/futures/*.cpp",
                "master/clone/folly/futures/detail/*.cpp",
                "master/clone/folly/io/*.cpp",
                "master/clone/folly/io/async/*.cpp",
                "master/clone/folly/stats/*.cpp"
            ],
            "sources!": [
                "master/clone/folly/detail/Clock.cpp",
                "master/clone/folly/wangle/*/*Test.cpp",
                "master/clone/folly/build/GenerateFingerprintTables.cpp"
            ],
            "defines": [
                "FOLLY_NO_CONFIG", # unless you run ./configure
                "FOLLY_VERSION=\"1\"", # ??? TODO
                "FOLLY_HAVE_MALLOC_USABLE_SIZE",
                # on ios?: "FOLLY_HAVE_MALLOC_SIZE"
                "FOLLY_HAVE_PTHREAD_ATFORK"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "master/clone"
                ],
                "cflags": [ 
                    "-std=c++11" # refuses to compile otherwise 
                ],
                "defines": [
                    "FOLLY_NO_CONFIG",
                    #"FOLLY_VERSION=\"1\"",
                    "FOLLY_HAVE_MALLOC_USABLE_SIZE",
                    # on ios?:
                    #"FOLLY_HAVE_MALLOC_SIZE"
                    "FOLLY_HAVE_PTHREAD_ATFORK"
                ]
            },
            "conditions": [
                ["OS=='linux'", {
                    "defines": ["FOLLY_HAVE_CLOCK_GETTIME"],
                    "link_settings" : {
                        "libraries" : [ "-ldl" ]
                    }
                }],
                ["OS=='win'", {
                    "defines": []
                }]
            ],
            "msvs_settings": {
                "VCCLCompilerTool": {
                    "WarningLevel": "0" # temporary!
                }
            },
            "export_dependent_settings": [
                "../glog/glog.gyp:*",
                "../gflags/gflags.gyp:*",
                "../pthread/pthread.gyp:*",
                "../double-conversion/double-conversion.gyp:*"
            ],
            "dependencies": [
                "../boost-regex/boost-regex.gyp:*",
                "../boost-function_types/boost-function_types.gyp:*",
                "../boost-filesystem/boost-filesystem.gyp:*",
                "../boost-mpl-type_traits-typeof-utility/boost-mpl-type_traits-typeof-utility.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-container/boost-container.gyp:*",
                "../boost-context/boost-context.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-variant/boost-variant.gyp:*",
                "../boost-thread/boost-thread.gyp:*",
                "../boost-numeric_conversion/boost-numeric_conversion.gyp:*",
                "../boost-intrusive/boost-intrusive.gyp:*",
                "../boost-lexical_cast-math/boost-lexical_cast-math.gyp:*",
                "../boost-crc/boost-crc.gyp:*",
                "../boost-conversion/boost-conversion.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-multi_index/boost-multi_index.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-algorithm/boost-algorithm.gyp:*",
                "../boost-random/boost-random.gyp:*",
                "../gflags/gflags.gyp:*",
                "../glog/glog.gyp:*",
                "../pthread/pthread.gyp:*",
                #"../openssl/openssl.gyp:*",
                "../double-conversion/double-conversion.gyp:*",
                "../libevent/libevent.gyp:*"
            ]
        },
        
        {
            "target_name": "folly_futures_test",
            "type": "executable",
            "test": {},
            "sources": [
                "master/clone/folly/futures/test/FutureTest.cpp",
                # g++ 4.8.2 failed for me on c9.io with internal compiler error.
                "master/clone/folly/futures/test/Thens.cpp",
                "master/clone/folly/futures/test/ExecutorTest.cpp"
            ],
            "dependencies": [
                "folly",
                 "../googlemock/googlemock.gyp:*",
                 "../googletest/googletest.gyp:*"
            ]
        }
    ]
}