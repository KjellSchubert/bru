{
    "targets": [
        {
            "target_name": "boost-tokenizer",
            "type": "none",
            "include_dirs": [
                "1.57.0/tokenizer-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/tokenizer-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }       
    ],
    "conditions": [
      ["OS!='iOS'", {
        "targets": [
        {
            "target_name": "boost-tokenizer_simple_example_1",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/tokenizer-boost-1.57.0/test/simple_example_1.cpp"
            ],
            "dependencies": [ "boost-tokenizer" ]
        }  
        ]
      }
      ]
    ]
}
