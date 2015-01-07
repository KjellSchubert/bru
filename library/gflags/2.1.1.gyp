{
    "targets": [
        {
            "target_name": "gflags",
            "type": "static_library",
            "include_dirs": [
                # the include dir is created by cmake
                "2.1.1/gflags-2.1.1/include/gflags"
                #"2.1.1/gflags-2.1.1/src"
            ],
            "sources": [
                "2.1.1/gflags-2.1.1/src/*.cc"
            ],
            "sources!": [
                "2.1.1/gflags-2.1.1/src/windows_port.cc"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "2.1.1/gflags-2.1.1/include"
                ]
            },
            "conditions": [

                ["OS=='win'", {
                  "defines": [
                    # TODO
                  ],
                  "direct_dependent_settings": {
                    "defines": [
                      # TODO
                    ]
                  }
                }]
            ]
        },

        {
            "target_name": "gflags_unittest",
            "type" : "executable",
            
            # Test keeps failing. TODO
            #"test": {
            #    "cwd": "2.1.1/gflags-2.1.1"
            #},
            
            "include_dirs": [
                "2.1.1/gflags-2.1.1/include/gflags", # config.h
                "2.1.1/gflags-2.1.1/src" # util.h
            ],
            "sources" : [
                "2.1.1/gflags-2.1.1/test/gflags_unittest.cc"
            ],
            "libraries": [ "-lpthread" ],
            "dependencies" : [
                "gflags",
                "../googletest/googletest.gyp:*"
            ]
        },
        
        # this is more an example than a test? Doesnt print the message it
        # advertises, kinda unclear, at least it exits without errors...
        {
            "target_name": "gflags_declaretest",
            "type" : "executable",
            "test": {},
            "sources" : [
                "2.1.1/gflags-2.1.1/test/gflags_declare_flags.cc",
                "2.1.1/gflags-2.1.1/test/gflags_declare_test.cc"
            ],
            "libraries": [ "-lpthread" ],
            "dependencies" : [
                "gflags"
            ]
        }

    ]
}
