{
    "targets": [
        {
            "target_name": "boost-functional",
            "type": "none",
            "include_dirs": [
                "1.62.0/functional-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/functional-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-integer/boost-integer.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-function_types/boost-function_types.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-assert/boost-assert.gyp:*"
            ]
        }
    ]
}
