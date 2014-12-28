{
    "targets": [
        {
            "target_name": "boost-exception",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/exception-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/exception-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/exception-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}