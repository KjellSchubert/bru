{
    "targets": [
        {
            "target_name": "boost-asio",
            "type": "none",
            "include_dirs": [
                "1.62.0/asio-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/asio-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-coroutine/boost-coroutine.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-chrono/boost-chrono.gyp:*",
                "../boost-date_time/boost-date_time.gyp:*"
            ]
        }
        
        # these examples gave me compile errors in a clang 3.4 / gcc 4.4 
        # gnu stdlib combination, so I'm temp disabling them.
        # TODO: consider fixing & reenabling these.
        
        # most of these tests are header-file self-containment tests?
        #{
        #    "target_name": "boost-asio_test_basic_stream_socket",
        #    "type": "executable",
        #    "test": {},
        #    "defines": [ "BOOST_ASIO_STANDALONE" ],
        #    "sources": [ "1.62.0/asio-boost-1.62.0/test/basic_stream_socket.cpp" ],
        #    "dependencies": [ "boost-asio" ]
        #},
        
        #{
        #    "target_name": "boost-asio_test_coroutine",
        #    "type": "executable",
        #    "test": {},
        #    "defines": [ "BOOST_ASIO_STANDALONE" ],
        #    "sources": [ "1.62.0/asio-boost-1.62.0/test/coroutine.cpp" ],
        #    "dependencies": [ "boost-asio" ]
        #},

        # does boost-asio require C++11? I didn't think so. But I couldnt get
        # cpp03/echo/async_tcp_echo_server.cpp to compile with clang 3.5,
        # neither with  nor without. The cpp11/ variant compiles
        # fine, but obviously requires 
        #{
        #    "target_name": "boost-asio_example_async_tcp_echo_server",
        #    "type": "executable",
        #    # is not an easily automatable test: you can telnet to the port
        #    # but I'm unsure how to trigger and end of the test.
        #    #"test": {},
        #    "cflags": [ "" ],
        #    "defines": [ "BOOST_ASIO_STANDALONE" ],
        #    "sources": [ "1.62.0/asio-boost-1.62.0/example/cpp11/echo/async_tcp_echo_server.cpp" ],
        #    "dependencies": [ "boost-asio" ]
        #}
    ]
}
