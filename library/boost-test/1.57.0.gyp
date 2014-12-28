{
    "targets": [
        {
            "target_name": "boost-test",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/test-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/test-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/test-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-lexical_cast/boost-lexical_cast.gyp:*",
                "../boost-io/boost-io.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-timer/boost-timer.gyp:*",
                "../boost-exception/boost-exception.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-test_exec_mon_example",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/test-boost-1.57.0/example/exec_mon_example.cpp"
            ],
            "dependencies": [ "boost-test" ]
        }

    ]
}