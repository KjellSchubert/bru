{
    "targets": [
        {
            "target_name": "boost-array",
            "type": "none",
            "include_dirs": [
                "1.57.0/array-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/array-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-array_array2",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/array-boost-1.57.0/test/array2.cpp" ],
            "dependencies": [ "boost-array" ]
        }
    ]
}