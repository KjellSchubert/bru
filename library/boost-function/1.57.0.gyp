{
    "targets": [
        {
            "target_name": "boost-function",
            "type": "none",
            "include_dirs": [
                "1.57.0/function-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/function-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-integer/boost-integer.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-bind/boost-bind.gyp:*"
            ]
        }
    ]
}