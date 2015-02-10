{
    "targets": [
        {
            "target_name": "boost-type_index",
            "type": "none",
            "include_dirs": [
                "1.57.0/type_index-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/type_index-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        }
    ],
    "conditions": [
      ["OS!='iOS'", {
        "targets": [
        {
            "target_name": "boost-type_index_ctti_print_name",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/type_index-boost-1.57.0/test/ctti_print_name.cpp"
            ],
            "dependencies": [ "boost-type_index" ]
        }  
        ]
      }
      ]
    ]
}
