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
                "2.0.1/RCF-2.0.1.101/src/RCF/BoostSystem.cpp"
            ]
        }
    ]
}