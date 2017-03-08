{
    "targets": [
        {
            "target_name": "boost-intrusive",
            "type": "none",
            "include_dirs": [
                "1.62.0/intrusive-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/intrusive-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*"
            ]
        }
        
        # Annoyingly there's another sort of dependency cycle here in the tests:
        # the tests #include boost/container and boost/container in turn depends
        # on boost/intrusive :( So cannot run these tests easily without merging
        # both modules into one.
        #{
        #    "target_name": "boost-intrusive_unordered_set_test",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.62.0/intrusive-boost-1.62.0/test/unordered_set_test.cpp" ],
        #    "dependencies": [ "boost-intrusive" ]
        #}
    ]
}
