{
    "targets": [
        {
            "target_name": "boost-smart_ptr",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/smart_ptr-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/smart_ptr-boost-1.62.0/include"
                ]
            },
            "sources": [
                "1.62.0/smart_ptr-boost-1.62.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-predef/boost-predef.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-align/boost-align.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}
