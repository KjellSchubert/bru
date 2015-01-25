{
    "targets": [
        {
            "target_name": "snappy",
            "type": "static_library",
            "defines": [ 
                # from Makefile after .configure:
                #"HAVE_CONFIG_H" 
            ],
            "include_dirs": [
                "1.1.1/snappy-1.1.1"
            ],
            "sources": [
                "1.1.1/snappy-1.1.1/*.cc"
            ],
            "sources!": [
                "1.1.1/snappy-1.1.1/*test*.cc"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.1.1/snappy-1.1.1"
                ]
            }
        },

        {
            "target_name": "snappy_unittest",
            "type": "executable",
            # Test is too slow with microbenchmarks enabled, so just compile
            # but dont run tests:
            #"test": {
            #    "cwd": "1.1.1/snappy-1.1.1"
            #    #"args": [ "--run_microbenchmarks=false" ] # if gflags was used
            #},
            "defines": [ 
                # from Makefile after .configure:
                #"HAVE_CONFIG_H" 
                # Or fixed config:
                "HAVE_SYS_TIME_H",
                "HAVE_SYS_RESOURCE_H"
                #"HAVE_GFLAGS",
                #"HAVE_GTEST"
                # instead of disabling the microbenchmarks via gflags we could 
                # also disabled via #define if there was an #ifdef around the
                # call to RunSpecifiedBenchmarks. But there isnt. So comment out
                # this line to just run the unit tests.
            ],
            "sources": [ 
                "1.1.1/snappy-1.1.1/snappy_unittest.cc", 
                "1.1.1/snappy-1.1.1/snappy-test.cc"
            ],
            "dependencies": [
                "snappy" 
                #"../gflags/gflags.gyp:*",
                #"../googletest/googletest.gyp:*"
            ]
        }
        
        # there's also snappy-test, which is benchmarking for speed?
    ]
}
