{
    "targets": [
        {
            "target_name": "boost-chrono",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/chrono-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/chrono-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/chrono-boost-1.57.0/src/*.cpp"
            ],
            "link_settings": {
                "libraries": [ "-lrt" ] # undefined reference to `clock_gettime'
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-winapi/boost-winapi.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-math/boost-math.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-ratio/boost-ratio.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-chrono_example_test_duration",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/chrono-boost-1.57.0/example/test_duration.cpp"
            ],
            "dependencies": [ "boost-chrono" ]
        },

        {
            "target_name": "boost-chrono_example_test_clock",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/chrono-boost-1.57.0/example/test_clock.cpp"
            ],
            "dependencies": [ "boost-chrono" ]
        }
    ]
}
