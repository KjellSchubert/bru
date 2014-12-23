{
    "includes": [ "bru_common.gypi" ],
    "targets": [

        {
            "target_name": "foo",
            "type": "static_library",
            "sources": [
                "foo/src/foo.cpp"
            ],
            "include_dirs": [
                "foo/include"
            ],
            "dependencies": [
                # to list deps on other external libs you'd write:
                #"bru_modules/boost-regex/boost-regex.gyp:*"
                #"bru_modules/ogg/ogg.gyp:*"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "foo/include"
                ]
            }
        },

        {
            "target_name": "foo-test",
            "type": "executable",
            "sources": [
                "foo/test/test.cpp"
            ],
            "dependencies": [
                "foo",   # thats the library target above
                "bru_modules/googletest/googletest.gyp:*" # an external dep
            ]
        }

    ]
}
