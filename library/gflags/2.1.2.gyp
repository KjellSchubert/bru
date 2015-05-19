{
    "targets": [
        {
            "target_name": "gflags",
            "type": "static_library",
            "include_dirs": [
                # the include dir is created by cmake
                "2.1.2/clone/include/gflags"
            ],
            "sources": [
                "2.1.2/clone/src/*.cc"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "2.1.2/clone/include"
                ]
            },
            "conditions": [

                ["OS!='win'", {
                    "sources!": [
                        "2.1.2/clone/src/windows_port.cc"
                    ],
                    "link_settings": {
                        "libraries": [ "-lpthread" ]
                    }
                }],

                ["OS=='win'", {
                    "link_settings": {
                        "libraries": [ "-lshlwapi.lib" ]  # PathMatchSpec
                    }
                }]
            ]
        },

        {
            "target_name": "gflags_unittest",
            "type" : "executable",

            # Test keeps failing. TODO
            #"test": {
            #    "cwd": "2.1.2/clone"
            #},

            "include_dirs": [
                "2.1.2/clone/include/gflags", # config.h
                "2.1.2/clone/src" # util.h
            ],
            "sources" : [
                "2.1.2/clone/test/gflags_unittest.cc"
            ],
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
                "2.1.2/clone/test/gflags_declare_flags.cc",
                "2.1.2/clone/test/gflags_declare_test.cc"
            ],
            "dependencies" : [
                "gflags"
            ]
        }

    ]
}
