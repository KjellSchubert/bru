{
    "targets": [
        {
            "target_name": "boost-multi_index",
            "type": "none",
            "include_dirs": [
                "1.57.0/multi_index-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/multi_index-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-serialization/boost-serialization.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-math/boost-math.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-foreach/boost-foreach.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-multi_index_test_basic",
            "type": "executable",
            "test": {},
            "sources": [ 
                "1.57.0/multi_index-boost-1.57.0/test/test_basic.cpp",
                "1.57.0/multi_index-boost-1.57.0/test/test_basic_main.cpp" 
            ],
            "dependencies": [ "boost-multi_index" ]
        },
        
        {
            "target_name": "boost-multi_index_example_basic",
            "type": "executable",
            "test": {},
            "sources": [ 
                "1.57.0/multi_index-boost-1.57.0/example/basic.cpp" 
            ],
            "dependencies": [ "boost-multi_index" ]
        }

    ]
}