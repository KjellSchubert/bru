{
    "targets": [
        {
            "target_name": "boost-io",
            "type": "none",
            "include_dirs": [
                "1.62.0/io-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/io-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*"
            ]
        }
        
        # TODO
        #{
        #    "target_name": "boost-io-ios_state_test",
        #    "type": "executable",
        #    "sources": ""
        #},
        
        # this depends on boost-test (see Jamfile reaching outside the module)
        #{
        #    "target_name": "boost-io-quoted_manip_test",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.62.0/io-boost-1.62.0/test/quoted_manip_test.cpp"
        #    ],
        #    "dependencies": [ "boost-io" ]
        #}

    ]
}
