{
    "targets": [
        {
            "target_name": "boost-logic",
            "type": "none",
            "include_dirs": [
                "1.57.0/logic-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/logic-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}