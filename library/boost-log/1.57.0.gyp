{
    "targets": [
        {
            "target_name": "boost-log",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/log-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/log-boost-1.57.0/include"
                ]
            },
            "defines": [
                # TODO: see http://www.boost.org/doc/libs/1_57_0/libs/log/doc/html/log/installation/config.html
                # e.g. the regex vs xpressive choice
            ],
            "sources": [
                "1.57.0/log-boost-1.57.0/src/*.cpp"
            ],
            "sources!": [
                # is this Windows-only?
                "1.57.0/log-boost-1.57.0/src/debug_output_backend.cpp",
                "1.57.0/log-boost-1.57.0/src/event_log_backend.cpp",
                # not compiling
                "1.57.0/log-boost-1.57.0/src/dump_avx2.cpp",
                "1.57.0/log-boost-1.57.0/src/dump_ssse3.cpp",
                "1.57.0/log-boost-1.57.0/src/init_from_settings.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-asio/boost-asio.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-phoenix/boost-phoenix.gyp:*",
                "../boost-function_types/boost-function_types.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-winapi/boost-winapi.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-fusion/boost-fusion.gyp:*",
                "../boost-parameter/boost-parameter.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-spirit/boost-spirit.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-xpressive/boost-xpressive.gyp:*",
                "../boost-thread/boost-thread.gyp:*",
                "../boost-filesystem/boost-filesystem.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-proto/boost-proto.gyp:*",
                "../boost-property_tree/boost-property_tree.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-lexical_cast/boost-lexical_cast.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-exception/boost-exception.gyp:*",
                "../boost-intrusive/boost-intrusive.gyp:*",
                "../boost-date_time/boost-date_time.gyp:*"
            ]
        }
        
        # TODO
        #{
        #    "target_name": "boost-log_test",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.57.0/log-boost-1.57.0/test/foooo.cpp" ],
        #    "dependencies": [ "boost-parameter" ]
        #}
    ]
}