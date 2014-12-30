{
    "targets": [
        {
            "target_name": "protobuf",
            "type": "static_library",
            "include_dirs": [
                "2.6.1/protobuf-2.6.1/src",
                "2.6.1/protobuf-2.6.1" # for config.h
            ],
            "sources": [
                "2.6.1/protobuf-2.6.1/src/google/protobuf/*.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/io/*.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/stubs/*.cc"
            ],
            "sources!": [
                "2.6.1/protobuf-2.6.1/src/google/protobuf/*unittest.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/io/*unittest.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/stubs/*unittest.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/test_util.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/test_util_lite.cc"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "2.6.1/protobuf-2.6.1/src"
                ]
            }
        },
        
        # this is the compiler for *.proto files
        {
            "target_name": "protoc",
            "type": "executable",
            "include_dirs": [
                "2.6.1/protobuf-2.6.1" # for config.h
            ],
            "sources": [
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/*.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/cpp/*.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/python/*.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/java/*.cc"
            ],
            "sources!": [
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/*unittest.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/mock_code_generator.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/test_plugin.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/cpp/*unittest.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/python/*unittest.cc",
                "2.6.1/protobuf-2.6.1/src/google/protobuf/compiler/java/*unittest.cc"
            ],
            "dependencies": [
                "protobuf"
            ]
        },
        
        {
            "target_name": "protobuf-example-list_people",
            "type": "executable",
            "include_dirs": [
                "2.6.1/protobuf-2.6.1/examples"
            ],
            "sources": [
                "2.6.1/protobuf-2.6.1/examples/list_people.cc",
                # this file was generated via
                #   >cd examples
                #   >protoc *.proto --cpp_out=.
                "2.6.1/protobuf-2.6.1/examples/addressbook.pb.cc"
            ],
            "dependencies": [ "protobuf", "protoc" ]
        },
        
        {
            "target_name": "protobuf-example-add_person",
            "type": "executable",
            "include_dirs": [
                "2.6.1/protobuf-2.6.1/examples"
            ],
            "sources": [
                "2.6.1/protobuf-2.6.1/examples/add_person.cc",
                "2.6.1/protobuf-2.6.1/examples/addressbook.pb.cc"
            ],
            "dependencies": [ "protobuf", "protoc" ]
        }

        
#        {
#            "target_name": "protobuf-test",
#            "type": "executable",
#            "test": {},
#            "include_dirs": [
#                #"2.6.1/protobuf-2.6.1" # for config.h
#            ],
#            "sources": [
#                "2.6.1/protobuf-2.6.1/src/google/protobuf/*unittest.cc",
#                "2.6.1/protobuf-2.6.1/src/google/protobuf/io/*unittest.cc",
#                "2.6.1/protobuf-2.6.1/src/google/protobuf/stubs/*unittest.cc",
#                "2.6.1/protobuf-2.6.1/src/google/protobuf/test_util.cc"
#            ],
#            "dependencies": [
#                "protobuf",
#                "../googletest/googletest.gyp:*"
#            ]
#        }
    ]
}
