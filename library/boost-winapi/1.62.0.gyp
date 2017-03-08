{
    "targets": [
        {
            "target_name": "boost-winapi",
            "type": "none",
            "include_dirs": [
                "1.62.0/winapi-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/winapi-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-predef/boost-predef.gyp:*"
            ]
        }
    ]
}
