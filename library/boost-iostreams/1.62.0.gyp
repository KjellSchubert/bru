{
    "targets": [
        {
            "target_name": "boost-iostreams",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/iostreams-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/iostreams-boost-1.62.0/include"
                ]
            },
            "sources": [
                "1.62.0/iostreams-boost-1.62.0/src/*.cpp"
            ],
            "sources!": [
                # From http://www.boost.org/doc/libs/1_62_0/libs/iostreams/doc/index.html
                # Compiling on Linux I didn't even realize there was a bzip
                # and zlib dependency, and Windows compilation failed. I'm
                # excluding the bzip dep for now to not get compiler errors
                # on Windows. Could enable this after importing bzip2 into bru.
                "1.62.0/iostreams-boost-1.62.0/src/bzip2.cpp" # NO_BZIP2
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-random/boost-random.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../zlib/zlib.gyp:*"
            ]
        },
        {
            "target_name": "boost-iostreams_back_inserter_example",
            "type": "executable",
            "test": {},
            "sources": [ "1.62.0/iostreams-boost-1.62.0/example/boost_back_inserter_example.cpp" ],
            "dependencies": [ "boost-iostreams"],
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
