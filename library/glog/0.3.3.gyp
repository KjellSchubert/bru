{
    "targets": [
        {
            "target_name": "glog",
            "type": "static_library",
            "include_dirs": [
                "0.3.3/glog-0.3.3/src"
            ],
            "sources": [
                "0.3.3/glog-0.3.3/src/*.cc"
            ],
            "sources!": [
                "0.3.3/glog-0.3.3/src/*test*.cc"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "0.3.3/glog-0.3.3/src"
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

        # one of the googletest samples also can serve as a rudimentary test:
        {
            "target_name": "glog_logging_unittest",
            "type" : "executable",
            "test": {
                "cwd": "0.3.3/glog-0.3.3"
            },
            "sources" : [
                "0.3.3/glog-0.3.3/src/logging_unittest.cc"
            ],
            "libraries": [ "-lpthread" ],
            "dependencies" : [
                "glog",
                "../googletest/googletest.gyp:*"
            ]
        }
    ]
}
