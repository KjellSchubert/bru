{
    "targets": [
        {
            "target_name": "boost-assert",
            "type": "none",
            "include_dirs": [
                "1.62.0/assert-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/assert-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*"
            ]
        }
    ]
}
