{
    "targets": [
        {
            "target_name": "boost-conversion",
            "type": "none",
            "include_dirs": [
                "1.62.0/conversion-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/conversion-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*"
            ]
        }
    ]
}
