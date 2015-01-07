{
    "targets": [
        {
            "target_name": "boost-crc",
            "type": "none",
            "include_dirs": [
                "1.57.0/crc-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/crc-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-integer/boost-integer.gyp:*"
            ]
        }
    ]
}