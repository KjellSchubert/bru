{
    "targets": [
        {
            "target_name": "boost-static_assert",
            "type": "none",
            "include_dirs": [
                "1.62.0/static_assert-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/static_assert-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*"
            ]
        }
    ]
}
