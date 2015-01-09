{
    "targets": [
        {
            # OpenSSL has a lot of config options, with some default options
            # enabling known insecure algorithms. What's a good combinations
            # of openssl config options?
            #   ./config no-asm no-shared no-ssl2 no-ssl3 no-hw no-zlib no-threads
            # ?
            # We don't use gyp to build openssl, but instead configure+make.
            # We only use gyp to collect build artifacts and specifiy 
            # include_dirs for downstream dependencies.
            
            "target_name": "openssl",
            "type": "none",
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.0.1j/openssl-1.0.1j/include"
                ]
            },
            # link against libssl.a and libcrypto.a
            "link_settings" : {
                # here's we use the same ugly pattern as for xerces to reference
                # the lib built via 'make' downstream: use a crappy 'copies'
                # into <(SHARED_INTERMEDIATE_DIR).
                "libraries" : [ "-lssl", "-lcrypto", "-lssl", "-ldl" ],
                "library_dirs": [ "<(SHARED_INTERMEDIATE_DIR)/libs" ]
            },
            # I dont like this pointless copying around, TODO: find a better 
            # solution
            "copies": [
                {
                    "destination": "<(SHARED_INTERMEDIATE_DIR)/libs",
                    "files": [ 
                        "1.0.1j/openssl-1.0.1j/libcrypto.a",
                        "1.0.1j/openssl-1.0.1j/libssl.a" 
                    ]
                }
            ]
        },
            
        # openssl has code for many separate test executables in the /test
        # dir, let's build a small subset of these via gyp to verify the
        # correctness of link_settings specified in the openssl gyp target.
        # This test loads data file and must be run with cwd=./test
        {
            "target_name": "ssltest",
            "type": "executable",
            "test": { 
                "cwd": "1.0.1j/openssl-1.0.1j/test"
            },
            "include_dirs": [
                "1.0.1j/openssl-1.0.1j" # e.g. e_os.h
            ],
            "sources": [
                # note how the ssl test depends on many #defines set via
                # ./configure. Do these need to be passed to the test build
                # explicitly? Apparently not.
                "1.0.1j/openssl-1.0.1j/test/ssltest.c"
            ],
            "dependencies": [ "openssl" ]
        },
        
        # compile one of the (interactive) openssl demo apps to verify correct
        # compiler & linker settings in upstream gyp target:
        {
            "target_name": "demos-easy_tls",
            "type": "executable",
            # not suitable as a test, just building this to see if it links
            #"test": { 
            #    "cwd": "1.0.1j/openssl-1.0.1j/demos/easy_tls"
            #},
            "include_dir": [ "1.0.1j/openssl-1.0.1j/demos/easy_tls" ],
            "sources": [ 
                "1.0.1j/openssl-1.0.1j/demos/easy_tls/test.c",
                "1.0.1j/openssl-1.0.1j/demos/easy_tls/easy-tls.c"
            ],
            "dependencies": [ "openssl" ]
        }
    ]
}
