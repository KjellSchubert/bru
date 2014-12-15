{
    "targets": [
        {
            "target_name": "boost-iterator",
            "type": "none",
            "include_dirs": [
                "1.57.0/iterator-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/iterator-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-conversion/boost-conversion.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-function_types/boost-function_types.gyp:*"
            ]
        }
    ]
}