{
    "targets": [
        {
            "target_name": "boost-ratio",
            "type": "none",
            "include_dirs": [
                "1.62.0/ratio-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/ratio-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-rational/boost-rational.gyp:*"
            ]
        }
        
        # This one doesnt compile witg gcc 4.8
        #{
        #    "target_name": "boost-ratio_test",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.62.0/ratio-boost-1.62.0/test/ratio_test.cpp"
        #    ],
        #    "dependencies": [ "boost-ratio" ]
        #}

    ]
}
