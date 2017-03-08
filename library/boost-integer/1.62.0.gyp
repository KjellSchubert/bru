{
    "targets": [
        {
            "target_name": "boost-integer",
            "type": "none",
            "include_dirs": [
                "1.62.0/integer-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/integer-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*"
            ]
        }
    ]
}
