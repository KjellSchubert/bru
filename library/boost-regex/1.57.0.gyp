{
    "targets": [
        {
            "target_name": "boost-regex",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/regex-boost-1.57.0/include"
            ],
            #"defines": [
            #    # this #define is needed for test/captures, it's not
            #    # a Boost default #define. Too much preprocessor-style 
            #    # customization for my taste. Without this flag the
            #    # capture test compilation fails with:
            #    # error: `boost::smatch' has no member named `captures'
            #    "BOOST_REGEX_MATCH_EXTRA"
            #],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/regex-boost-1.57.0/include"
                ]
                # supposedly all downstream compilation units need to be
                # be using the same #define (otherwise ODR violation? or
                # just linker errors?)
                #"defines": [
                #    "BOOST_REGEX_MATCH_EXTRA"
                #]
            },
            "sources": [
                "1.57.0/regex-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-functional/boost-functional.gyp:*"
            ]
        }

        # Adding this test will cause circular dep problems, since pulling
        # in boost-test will cause lots of additional deps, including to 
        # boost-regex. I had temporarily removed the boost-test dependency
        # from this test (just a handful of changes btw) and it passed.
        # TODO: reenable this test after circular deps were fixed in 
        # modularized Boost.
        #{
        #    "target_name": "boost-regex_captures_test",
        #    "type": "executable",
        #    "sources": [
        #        "1.57.0/regex-boost-1.57.0/test/captures/captures_test.cpp"
        #    ],
        #    "dependencies": [
        #        "boost-regex"
        #    ]
        #}
    ]
}
