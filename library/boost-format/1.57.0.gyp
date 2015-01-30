{
    "targets": [
        {
            "target_name": "boost-format",
            "type": "none",
            "include_dirs": [
                "1.57.0/format-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/format-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        }
        
        # TODO: add tests once boost-test dependency cycles are sorted out
    ],    
    "conditions": [
      ["OS!='iOS'", 
        {
            "target_name": "boost-format_sample_formats",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/format-boost-1.57.0/example/sample_formats.cpp" ],
            "dependencies": [ "boost-format" 
            ]
        }
      ] 
    ]
}
