{
    "targets": [
        {
            "target_name": "boost-system",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/system-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/system-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/system-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ],
    "conditions": [
      ["OS!='iOS'", {
        "targets": [
        {
            "target_name": "boost-system_error_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/system-boost-1.57.0/test/system_error_test.cpp"
            ],
            "dependencies": [ "boost-system" ]
        }  
        ]
      }
      ]
    ]
}