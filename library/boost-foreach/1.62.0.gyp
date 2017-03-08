{
    "targets": [
        {
            "target_name": "boost-foreach",
            "type": "none",
            "include_dirs": [
                "1.62.0/foreach-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/foreach-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }

        # this test asserts/fails with msvs 2012
        #{
        #    "target_name": "boost-foreach_noncopyable",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.62.0/foreach-boost-1.62.0/test/noncopyable.cpp"
        #    ],
        #    "dependencies": [ "boost-foreach" ]
        #}
    ]
}
