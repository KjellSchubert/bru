{
    "targets": [
        {
            "target_name": "boost-align",
            "type": "none",
            "include_dirs": [
                "1.62.0/align-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/align-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*"
            ]
        }
    ]
}
