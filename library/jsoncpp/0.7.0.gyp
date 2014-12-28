{
    "targets": [
        {
            "target_name": "jsoncpp",
            "type": "static_library",
            "include_dirs": [
                "0.7.0/jsoncpp-0.7.0/include"
            ],
            "sources": [
                "0.7.0/jsoncpp-0.7.0/src/lib_json/*.cpp"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "0.7.0/jsoncpp-0.7.0/include"
                ]
            }
        },

        {
            "target_name": "jsoncpp_test",
            "type" : "executable",
            "test": {},
            "sources" : [
                "0.7.0/jsoncpp-0.7.0/src/test_lib_json/*.cpp"
            ],
            "dependencies" : [ "jsoncpp" ]
        }
        
        # just a utility, not a test in itself. To be run together with 
        # python tests. Which aren't being run yet, so this build is kinda
        # pointless.
        #{
        #    "target_name": "jsoncpp_testrunner",
        #    "type" : "executable",
        #    "sources" : [ "0.7.0/jsoncpp-0.7.0/src/test_lib_json/*.cpp" ],
        #    "dependencies" : [ "jsoncpp" ]
        #}

    ]
}
