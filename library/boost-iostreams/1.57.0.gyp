{
    "targets": [
        {
            "target_name": "boost-iostreams",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/iostreams-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/iostreams-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/iostreams-boost-1.57.0/src/*.cpp"
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
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-iostreams_back_inserter_example",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/iostreams-boost-1.57.0/example/boost_back_inserter_example.cpp" ],
            "dependencies": [ "boost-iostreams" ]
        }
    ]
}