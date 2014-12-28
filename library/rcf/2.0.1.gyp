{
    # This is work in progress, doesnt compile with gcc 4.8.2 atm.
    # The way RCF tries to handle its Boost dependency is interesting...

    "targets" : [
        {
            "target_name": "rcf",
            "type": "static_library",
            "include_dirs" : [
                "2.0.1/RCF-2.0.1.101/include"
            ],
            "defines": [
                # see http://www.deltavsoft.com/doc/rcf_user_guide/AppendixBuilding.html
                # for available #defines
                #"RCF_USE_OPENSSL",
                #"RCF_OPENSSL_STATIC"
                #"RCF_USE_ZLIB"
                #"RCF_ZLIB_STATIC"
            ],
            "sources": [
                "2.0.1/RCF-2.0.1.101/src/RCF/*.cpp"
            ],
            
            # initially I wanted to spec sources like this:
            #   "2.0.1/RCF-2.0.1.101/src/RCF/*.cpp"
            # but it turned out that RCF includes boost sources in a funky
            # way in RCF/BoostFilesystem.cpp instead of just declaring a
            # dependency against Boost.
            # So this statement here excludes these explicit Boost cpp #includes:
            "sources!": [
                "2.0.1/RCF-2.0.1.101/src/RCF/BoostFilesystem.cpp",
                "2.0.1/RCF-2.0.1.101/src/RCF/BoostSystem.cpp",
                
                # don't want to build a DLL:
                "2.0.1/RCF-2.0.1.101/src/RCF/DynamicLib.cpp",
                
                # complains about RCF_FEATURE_FILETRANSFER not being 1
                "2.0.1/RCF-2.0.1.101/src/RCF/FileStream.cpp",
                "2.0.1/RCF-2.0.1.101/src/RCF/FileTransferService.cpp"
            ],
            
            "dependencies": [
                "../boost-filesystem/boost-filesystem.gyp:*"
            ]
        }
    ]
}