{
    "targets": [
        {
            "target_name": "boost-thread",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/thread-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/thread-boost-1.57.0/include"
                ]
            },
            "defines": [
                # necessary for windows build, otherwise you get
                # unresolved external symbol "void __cdecl boost::tss_cleanup_implemented
                "BOOST_THREAD_BUILD_LIB"
            ],
            "sources": [
                "1.57.0/thread-boost-1.57.0/src/*.cpp"
            ],
            # there are 2 subdirs in src: one pthread, one win32. Since they
            # have the same file names we have to conditionally include them:
            "conditions": [
                ["OS=='win'", {
                    "sources": [ "1.57.0/thread-boost-1.57.0/src/win32/*.cpp" ]
                }, {
                    # OS!='win'
                    "sources": [ "1.57.0/thread-boost-1.57.0/src/pthread/*.cpp" ],
                    "link_settings": {
                        "libraries": [ "-lpthread" ]
                    }
                }]
            ],

            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-atomic/boost-atomic.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-winapi/boost-winapi.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-io/boost-io.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-container/boost-container.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-exception/boost-exception.gyp:*",
                "../boost-chrono/boost-chrono.gyp:*",
                "../boost-intrusive/boost-intrusive.gyp:*",
                "../boost-date_time/boost-date_time.gyp:*"
            ]
        },

        {
            "target_name": "boost-thread_test_futures",
            "type": "executable",
            # this test runs painfully slowly (30sec), disabling it
            #"test": {},
            "sources": [
                "1.57.0/thread-boost-1.57.0/test/test_futures.cpp"
            ],
            "dependencies": [
                "../boost-test/boost-test.gyp:*",
                "boost-thread"
            ]
        },

        {
            "target_name": "boost-thread_test_thread_launching",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/thread-boost-1.57.0/test/test_thread_launching.cpp"
            ],
            "dependencies": [
                "../boost-test/boost-test.gyp:*",
                "boost-thread"
            ]
        }

    ]
}
