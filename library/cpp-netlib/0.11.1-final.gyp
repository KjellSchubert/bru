{
    "targets": [
        {
            "target_name": "cpp-netlib",
            "type": "static_library", # unlike boost-asio which is header-only
            "include_dirs": [
                "0.11.1-final/cpp-netlib-cpp-netlib-0.11.1-final"
            ],
            "defines": [
                "BOOST_NETWORK_ENABLE_HTTPS" # otherwise getting "HTTPS not supported"
            ],
            "sources": [
                "0.11.1-final/cpp-netlib-cpp-netlib-0.11.1-final/libs/network/src/*.cpp",
                "0.11.1-final/cpp-netlib-cpp-netlib-0.11.1-final/libs/network/src/*/*.cpp"
            ],
            "sources!": [
                # I'm getting internal compiler errors with clang 3.5 and gcc 4.8.2
                # on uri.cpp after compiling for minutes. This uri.cpp uses 
                # boost-spirit, which is a bit of an ICE-magnet :(
                # See also https://github.com/cpp-netlib/cpp-netlib/issues/133
                # and http://stackoverflow.com/questions/2616011/easy-way-to-parse-a-url-in-c-cross-platform
                # Anyway, cannot exlude it from build, yields linker errors.
                #"0.11.1-final/cpp-netlib-cpp-netlib-0.11.1-final/libs/network/src/uri/uri.cpp"
            ],
            "direct_dependent_settings": {
                "defines": [
                    "BOOST_NETWORK_ENABLE_HTTPS"
                ],
                "include_dirs": [
                    "0.11.1-final/cpp-netlib-cpp-netlib-0.11.1-final"
                ]
            },
            "dependencies": [
                "../boost-asio/boost-asio.gyp:boost-asio",
                "../boost-assign/boost-assign.gyp:boost-assign",
                "../boost-logic/boost-logic.gyp:boost-logic"
            ],
            "export_dependent_settings": [
                "../boost-asio/boost-asio.gyp:boost-asio",
                "../boost-assign/boost-assign.gyp:boost-assign",
                "../boost-logic/boost-logic.gyp:boost-logic"
            ]
        },

        {
            "target_name": "cpp-netlib_simple_wget",
            "type" : "executable",
            "test": {
                "args": []
            },
            "sources" : [
                "0.11.1-final/cpp-netlib-cpp-netlib-0.11.1-final/libs/network/example/simple_wget.cpp"
            ],
            "dependencies" : [
                "cpp-netlib",
                "../openssl/openssl.gyp:*" # only needed for https GETs
            ]
        }
    ]
}

