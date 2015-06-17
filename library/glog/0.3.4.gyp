{
    "targets": [
        {
            "target_name": "glog",
            "type": "static_library",
            "include_dirs": [
                "0.3.4/clone/src"
            ],
            "sources": [
                "0.3.4/clone/src/*.cc"
            ],
            "sources!": [
                "0.3.4/clone/src/*test*.cc"
            ],
            "conditions": [

                ["OS=='win'", {
                    "include_dirs": [
                        "0.3.4/clone/src/windows"
                    ],
                    "sources": [
                        "0.3.4/clone/src/windows/*.cc"
                    ],
                    "direct_dependent_settings": {
                        "include_dirs": [
                            "0.3.4/clone/src/windows"
                        ]
                    }
                }],

                ["OS!='win'", {
                    "direct_dependent_settings": {
                        "include_dirs": [
                            "0.3.4/clone/src"
                        ]
                    },
                    "link_settings": {
                        "libraries": [ "-lpthread" ]
                    }
                }]
            ]
        },

        # one of the googletest samples also can serve as a rudimentary test:
        {
            "target_name": "glog_logging_unittest",
            "type" : "executable",
            "test": {
                "cwd": "0.3.4/clone/src/glog"
            },
            "sources" : [
                "0.3.4/clone/src/logging_unittest.cc"
            ],
            "conditions": [

                ["OS=='win'", {
                    "include_dirs": [
                        "0.3.4/clone/src/windows"
                    ]
                }]
            ],
            "dependencies" : [
                "glog",
                "../googletest/googletest.gyp:*"
            ]
        }
    ]
}
