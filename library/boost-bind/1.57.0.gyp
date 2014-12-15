{
    "targets": [
        {
            "target_name": "boost-bind",
            "type": "none",
            "include_dirs": [
                "1.57.0/bind-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/bind-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}