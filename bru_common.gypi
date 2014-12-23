{
    # Explicit default options for MSVC builds. Gyp itself does not
    # specify a lot of default project options for MSVC, to the point that
    # a simple type="executable" target won't even link with error
    #   LNK1561 entry point must be defined
    # because of missing /SUBSYSTEM:CONSOLE linker option.
    #
    # These defaults here were copied partially from
    #   https://github.com/joyent/node/blob/v0.10.26/common.gypi#L151
    "variables": {
        "target_arch%": "ia32"
    },
    "target_defaults": {
        "msvs_settings": {
            "VCCLCompilerTool": {
                "RuntimeLibrary": 0, # static release
                "Optimization": 3, # /Ox, full optimization
                "FavorSizeOrSpeed": 1, # /Ot, favour speed over size
                "InlineFunctionExpansion": 2, # /Ob2, inline anything eligible
                "WholeProgramOptimization": "true", # /GL, whole program optimization, needed for LTCG
                "OmitFramePointers": "true",
                "EnableFunctionLevelLinking": "true",
                "EnableIntrinsicFunctions": "true",
                "ExceptionHandling": 1 # /EHsc
                #"RuntimeTypeInfo": "false",
            },
            "VCLibrarianTool": {
                "AdditionalOptions": [
                    "/LTCG" # link time code generation
                ]
            },
            "VCLinkerTool": {
                "conditions": [
                      ["target_arch=='x64'", {
                            "TargetMachine" : 17 # /MACHINE:X64
                      }]
                ],
                "GenerateDebugInformation": "true",
                #"RandomizedBaseAddress": 2, # enable ASLR
                #"DataExecutionPrevention": 2, # enable DEP
                #"AllowIsolation": "true",
                "SuppressStartupBanner": "true",
                "LinkTimeCodeGeneration": 1, # link-time code generation
                "OptimizeReferences": 2, # /OPT:REF
                "EnableCOMDATFolding": 2, # /OPT:ICF
                "LinkIncremental": 1, # disable incremental linking
                "target_conditions": [
                    ["_type=='executable'", {
                        "SubSystem": 1 # console executable
                    }]
                ]
            }
        }
    }
}
