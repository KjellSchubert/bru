{
    "targets": [
        {
            "target_name": "boost-optional",
            "type": "none",
            "include_dirs": [
                "1.62.0/optional-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/optional-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-move/boost-move.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}
