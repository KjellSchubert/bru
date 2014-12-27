{
    "targets": [
        {
            "target_name": "boost-any",
            "type": "none",
            "include_dirs": [
                "1.57.0/any-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/any-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-type_index/boost-type_index.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-any_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/any-boost-1.57.0/test/any_test.cpp"
            ],
            "dependencies": [ "boost-any" ]
        }
    ]
}