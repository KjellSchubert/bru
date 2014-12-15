{
    "targets": [
        {
            "target_name": "googletest",
            "type": "static_library",
            "defines" : [
                # not sure what pthreads buys us (optional parallel test
                # execution?). Since googletest doesn't use std::thread yet
                # afaik I'm not sure if this even compiles on windows without
                # this #define. May wanna reconsider disabling this across
                # all platforms. Todo?
                "GTEST_HAS_PTHREAD=0"
            ],
            "include_dirs": [
                "1.7.0/gtest-1.7.0/include",

                # Needed for src/gtest-internal-inl.h.
                # Note that downstream clients will not see that file.
                "1.7.0/gtest-1.7.0"
            ],
            "sources": [
                # here we cannot reference *.cc since the src dir contains
                # the funky gtest-all.cc which #includes everything. Of course
                # we can just reference this gtest-all.cc here:
                "1.7.0/gtest-1.7.0/src/gtest-all.cc",
                "./1.7.0/gtest-1.7.0/src/gtest_main.cc"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.7.0/gtest-1.7.0/include"
                    # 1.7.0/gtest-1.7.0[/src] is not in here on purpose
                ],
                "defines": [
                    "GTEST_HAS_PTHREAD=0"
                ]
            }
        },

        # This is one of the lib's own tests, it compiles but has
        # one failure 'OutputFileHelpersTest.GetCurrentExecutableName'
        #{
        #    "target_name": "googletest_test",
        #    "type": "executable",
        #    "include_dirs": [
        #        # only needed because gtest_all_test.cc includes other
        #        # files from test/ via #include "test/foo.cc"
        #        "1.7.0/gtest-1.7.0"
        #    ],
        #    "sources": [ 
        #        "1.7.0/gtest-1.7.0/test/gtest_all_test.cc" 
        #    ],
        #    "dependencies": [
        #        "googletest"
        #    ]
        #}

        # one of the googletest samples also can serve as a rudimentary test:
        {
            "target_name": "googletest_sample1",
            "type" : "executable",
            "include_dirs" : [
                "1.7.0/gtest-1.7.0/samples/"
            ],
            "sources" : [
                "1.7.0/gtest-1.7.0/samples/sample1.cc",
                "1.7.0/gtest-1.7.0/samples/sample1_unittest.cc"
            ],
            "dependencies" : [
                "googletest"
            ]
        }
    ]
}
