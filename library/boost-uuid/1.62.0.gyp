{
    "targets": [
        {
            "target_name": "boost-uuid",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/uuid-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/uuid-boost-1.62.0/include"
                ]
            },
            "sources": [
            ],
            "dependencies": [
                "../boost-io/boost-io.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-chrono/boost-chrono.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}
