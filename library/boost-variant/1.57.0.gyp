{
    "targets": [
        {
            "target_name": "boost-variant",
            "type": "none",
            "include_dirs": [
                "1.57.0/variant-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/variant-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-math/boost-math.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-type_index/boost-type_index.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-variant_recursive_variant_test",
            "type": "executable",
            "test": {},
            "sources": [ 
                "1.57.0/variant-boost-1.57.0/test/recursive_variant_test.cpp"
            ],
            "dependencies": [ 
                "boost-variant",
                "../boost-test/boost-test.gyp:*"
            ]
        }
    ]
}