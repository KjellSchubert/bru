{
    "targets": [
        {
            "target_name": "cpp-netlib",
            "type": "static_library", # unlike boost-asio which is header-only
            "include_dirs": [
                "0.10.1/cpp-netlib-cpp-netlib-0.10.1"
            ],
            "defines": [
                "BOOST_NETWORK_ENABLE_HTTPS" # otherwise getting "HTTPS not supported"
            ],
            "sources": [
                "0.10.1/cpp-netlib-cpp-netlib-0.10.1/libs/network/src/*.cpp",
                "0.10.1/cpp-netlib-cpp-netlib-0.10.1/libs/network/src/*/*.cpp"
            ],
            "direct_dependent_settings": {
                "defines": [
                    "BOOST_NETWORK_ENABLE_HTTPS"
                ],
                "include_dirs": [
                    "0.10.1/cpp-netlib-cpp-netlib-0.10.1"
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
                "0.10.1/cpp-netlib-cpp-netlib-0.10.1/libs/network/example/simple_wget.cpp"
            ],
            "dependencies" : [
                "cpp-netlib",
                "../openssl/openssl.gyp:*" # only needed for https GETs
            ]
        }
    ]
}
