{
    "targets": [
        {
            "target_name": "boost-unordered",
            "type": "none",
            "include_dirs": [
                "1.57.0/unordered-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/unordered-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-container/boost-container.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }        
    ],
        "conditions": [
      ["OS!='iOS'", {
            "target_name": "boost-unordered_erase_tests",
            "type": "executable",
            "test": {},
            "sources": [ 
                "1.57.0/unordered-boost-1.57.0/test/unordered/erase_tests.cpp"
            ],
            "dependencies": [ "boost-unordered"             
            ]
        }
      ] 
    ]
}
