{
    "targets": [
        {
            "target_name": "boost-throw_exception",
            "type": "none",
            "include_dirs": [
                "1.57.0/throw_exception-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/throw_exception-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*"
            ]
        }
    ]
}