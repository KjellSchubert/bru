{
    "targets": [
        {
            "target_name": "boost-coroutine",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/coroutine-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/coroutine-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/coroutine-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-context/boost-context.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-exception/boost-exception.gyp:*"
            ]
        }
        
        # tests & examples have too many deps for my taste, not including
        # tests for now. 
        #{
        #    "target_name": "boost-coroutine_test_symm",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.57.0/coroutine-boost-1.57.0/test/test_symmetric_coroutine.cpp"
        #    ],
        #    "dependencies": [
        #        "boost-coroutine",
        #        "../boost-test/boost-test.gyp:*"
        #    ]
        #}
    ]
}