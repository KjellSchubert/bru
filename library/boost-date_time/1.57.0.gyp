{
    "targets": [
        {
            "target_name": "boost-date_time",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/date_time-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/date_time-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/date_time-boost-1.57.0/src/**/*.cpp"
            ],
            "dependencies": [
                "../boost-tokenizer/boost-tokenizer.gyp:*",
                "../boost-config/boost-config.gyp:*",
                #"../boost-serialization/boost-serialization.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-algorithm/boost-algorithm.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-lexical_cast/boost-lexical_cast.gyp:*",
                "../boost-io/boost-io.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        }        
    ],    
    "conditions": [
      ["OS!='iOS'", 
        {
            "target_name": "gregorian_testparse_date",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/date_time-boost-1.57.0/test/gregorian/testparse_date.cpp" 
            ],
            "dependencies": [ "boost-date_time" 
            ]
        }
      ] 
    ]
}
