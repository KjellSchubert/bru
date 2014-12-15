{
    "targets": [
        {
            "target_name": "boost-move",
            "type": "none",
            "include_dirs": [
                "1.57.0/move-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/move-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}