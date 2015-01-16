{
    "targets": [
        {
            "target_name": "libxml2",
            "type": "static_library",
            "include_dirs": [
                "2.9.2/libxml2-2.9.2/include"
            ],
            "defines": [
                # from generated makefile
                "HAVE_CONFIG_H"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "2.9.2/libxml2-2.9.2/include"
                ]
            },
            "sources": [ "2.9.2/libxml2-2.9.2/*.c" ],
            "sources!": [
                "2.9.2/libxml2-2.9.2/*test*.c", # compile test in separate target
                "2.9.2/libxml2-2.9.2/runsuite.c", # testrunner's main()

                # some utils providing main()
                "2.9.2/libxml2-2.9.2/runxmlconf.c", # yet another main()
                "2.9.2/libxml2-2.9.2/xmlcatalog.c",
                "2.9.2/libxml2-2.9.2/xmllint.c",

                "2.9.2/libxml2-2.9.2/trio.c" # doesnt compile, make doesnt build it
            ],
            
            "dependencies": [
                "../zlib/zlib.gyp:*"
            ]
        },
        
        {
            "target_name": "libxml2-testSAX",
            "type": "executable",
            "test": {},
            "sources": [ "2.9.2/libxml2-2.9.2/testSAX.c" ],
            "dependencies": [ "libxml2" ]
        },
        
        {
            "target_name": "libxml2-testXPath",
            "type": "executable",
            "test": {},
            "sources": [ "2.9.2/libxml2-2.9.2/testXPath.c" ],
            "dependencies": [ "libxml2" ]
        },
        
        {
            "target_name": "libxml2-example",
            "type": "executable",
            "test": {},
            "sources": [ "2.9.2/libxml2-2.9.2/example/gjobread.c" ],
            "dependencies": [ "libxml2" ]
        }
    ]
}
