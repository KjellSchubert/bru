{
    "targets": [
        {
            "target_name": "boost-test",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/test-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/test-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/test-boost-1.57.0/src/*.cpp"
            ],
            # See Jamfile.v2 with UTF_SOURCES: this does not contain cpp_main.
            # Apparently this cpp_main is not to be used for the static lib
            # builds of boost-test? Confusingly if you compile & link this 
            # cpp_main.cpp into a static boost-test build you'll get gcc 
            # linker errors about a missing cpp_main() function, not about
            # the duplicate main().
            "sources!": [
                "1.57.0/test-boost-1.57.0/src/cpp_main.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-lexical_cast/boost-lexical_cast.gyp:*",
                "../boost-io/boost-io.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-timer/boost-timer.gyp:*",
                "../boost-exception/boost-exception.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }
    ],
    "conditions": [
      ["OS!='iOS'", 
        {
            "target_name": "boost-test_unit_test_example_01",
            "type": "executable",
            # Compiles & runs but this example is designed to fail, so not
            # enabling this as a test:
            #"test": {},
            "sources": [
                "1.57.0/test-boost-1.57.0/example/unit_test_example_01.cpp"
            ],
            "dependencies": [ "boost-test" ]
        },

        {
            "target_name": "boost-test_result_report_test",
            "type": "executable",
            "test": {
                # cwd is important, test reads files
                "cwd": "1.57.0/test-boost-1.57.0/test"
            },
            "sources": [
                "1.57.0/test-boost-1.57.0/test/result_report_test.cpp"
            ],
            "dependencies": [ "boost-test" ]
        },
        
        {
            "target_name": "boost-test_algorithms_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/test-boost-1.57.0/test/algorithms_test.cpp"
            ],
            "dependencies": [ "boost-test" ]
        },

        {
            "target_name": "boost-test_test_case_template_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/test-boost-1.57.0/test/test_case_template_test.cpp"
            ],
            "dependencies": [ "boost-test" 
            ]
        }
      ] 
    ]
}
