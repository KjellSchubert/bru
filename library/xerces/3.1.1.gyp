{
    "targets": [
        {
            "target_name": "xerces",
            "type": "static_library",
            "include_dirs": [
                "3.1.1/xerces-c-3.1.1/src",
                "3.1.1/xerces-c-3.1.1", # ./config.h only
                "3.1.1/xerces-c-3.1.1/src/xercesc/util" # from Makefile, kinda odd
            ],
            "defines": [
                # common across all platforms:
                "XERCES_BUILDING_LIBRARY"
                # platform-specific defines are listed in conditions below.
            ],
            # Initially I tried to compile this via gyp, but the *.c files that
            # masquerade as *.cpp files spoiled that plan. Just 'make' for now.
            #"sources": [
            # P.S.: then I ran into problems with mixing msbuild & nmake and
            # gyp on Windows (ImageHasSafeExceptionHandlers) and used
            #   >python3 ~/bru/vcproj2gyp.py ..VC10\xerces-all\XercesLib\XercesLib.vcxproj "Static Release" Win32
            # to extract a list of cpp files from the Windows *.vcproj, and
            # intersected this with Linux files generated from make -n. Exact
            # script steps here:
            #    >cd bru_modules/xerces # here the module's gyp is located
            #    >pushd .
            #    >cd cd bru_modules/xerces/3.1.1/xerces-c-3.1.1/src/
            #    >make -n > make.log
            #    >popd
            #    >~/bru/makefile2gyp.py 3.1.1/xerces-c-3.1.1/src/make.log > linuxsrc.gyp
            #    >~/bru/vcproj2gyp.py 3.1.1\xerces-c-3.1.1\projects\Win32\VC10\xerces-all\XercesLib\XercesLib.vcxproj "Static Release" Win32 > windowssrc.gyp
            #    >~/bru/gyp_sources_intersect.py windowssrc.gyp linuxsrc.gyp
            "sources": [
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/Base64.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/BinFileInputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/BinInputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/BinMemInputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/BitSet.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/DefaultPanicHandler.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/EncodingValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/HeaderDummy.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/HexBin.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/KVStringPair.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/Mutexes.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/PanicHandler.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/PlatformUtils.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/PSVIUni.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/QName.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/StringPool.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/SynchronizedStringPool.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/TransService.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMemory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XML256TableTranscoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XML88591Transcoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLAbstractDoubleFloat.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLASCIITranscoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLBigDecimal.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLBigInteger.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLChar.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLChTranscoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLDateTime.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLDouble.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLEBCDICTranscoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLException.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLFloat.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLIBM1047Transcoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLIBM1140Transcoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLInitializer.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLMsgLoader.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLNumber.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLString.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLStringTokenizer.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLUCS4Transcoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLUni.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLUri.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLURL.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLUTF16Transcoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLUTF8Transcoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/XMLWin1252Transcoder.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/MsgLoaders/InMemory/InMemMsgLoader.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/BinHTTPInputStreamCommon.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/ASCIIRangeFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/BlockRangeFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/BMPattern.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/CharToken.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/ClosureToken.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/ConcatToken.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/Match.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/Op.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/OpFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/ParenToken.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/ParserForXMLSchema.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/RangeFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/RangeToken.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/RangeTokenMap.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/RegularExpression.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/RegxParser.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/RegxUtil.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/StringToken.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/Token.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/TokenFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/UnicodeRangeFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/UnionToken.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/XMLRangeFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/regx/XMLUniCharacter.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/LocalFileFormatTarget.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/LocalFileInputSource.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/MemBufFormatTarget.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/MemBufInputSource.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/StdInInputSource.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/StdOutFormatTarget.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/URLInputSource.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/Wrapper4DOMLSInput.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/Wrapper4InputSource.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLAttDef.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLAttDefList.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLAttr.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLBuffer.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLBufferMgr.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLContentModel.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLDTDDescription.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLElementDecl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLEntityDecl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLFormatter.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLGrammarDescription.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLGrammarPoolImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLNotationDecl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLRecognizer.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLRefInfo.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLSchemaDescription.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/XMLValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/PSVIAttribute.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/PSVIAttributeList.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/PSVIElement.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/PSVIItem.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSAnnotation.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSAttributeDeclaration.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSAttributeGroupDefinition.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSAttributeUse.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSComplexTypeDefinition.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSElementDeclaration.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSFacet.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSIDCDefinition.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSModel.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSModelGroup.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSModelGroupDefinition.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSMultiValueFacet.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSNamespaceItem.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSNotationDeclaration.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSObject.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSParticle.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSSimpleTypeDefinition.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSTypeDefinition.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSValue.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/psvi/XSWildcard.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/BinFileOutputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/BinMemOutputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/framework/BinOutputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/DGXMLScanner.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/ElemStack.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/IGXMLScanner.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/IGXMLScanner2.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/MemoryManagerImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/ReaderMgr.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/SGXMLScanner.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/ValidationContextImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/VecAttributesImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/VecAttrListImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/WFXMLScanner.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XMLReader.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XMLScanner.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XMLScannerResolver.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XProtoType.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XSAXMLScanner.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XSerializeEngine.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XSObjectFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/internal/XTemplateSerializer.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/sax/Dummy.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/sax/InputSource.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/sax/SAXException.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/sax/SAXParseException.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/parsers/AbstractDOMParser.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/parsers/DOMLSParserImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/parsers/SAX2XMLFilterImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/parsers/SAX2XMLReaderImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/parsers/SAXParser.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/parsers/XercesDOMParser.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/AllContentModel.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/CMAny.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/CMBinaryOp.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/CMUnaryOp.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/ContentLeafNameTypeVector.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/ContentSpecNode.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/DFAContentModel.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/Grammar.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/GrammarResolver.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/MixedContentModel.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/common/SimpleContentModel.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/AbstractNumericFacetValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/AbstractNumericValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/AbstractStringValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/AnySimpleTypeDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/AnyURIDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/Base64BinaryDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/BooleanDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DatatypeValidatorFactory.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DateDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DateTimeDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DateTimeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DayDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DecimalDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DoubleDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/DurationDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/ENTITYDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/FloatDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/HexBinaryDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/IDDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/IDREFDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/ListDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/MonthDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/MonthDayDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/NameDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/NCNameDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/NOTATIONDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/QNameDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/StringDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/TimeDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/UnionDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/XMLCanRepGroup.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/YearDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/datatype/YearMonthDatatypeValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/DTDAttDef.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/DTDAttDefList.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/DTDElementDecl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/DTDEntityDecl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/DTDGrammar.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/DTDScanner.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/DTDValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/DTD/XMLDTDDescriptionImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/ComplexTypeInfo.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/GeneralAttributeCheck.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/NamespaceScope.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SchemaAttDef.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SchemaAttDefList.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SchemaElementDecl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SchemaGrammar.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SchemaInfo.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SchemaSymbols.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SchemaValidator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/SubstitutionGroupComparator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/TraverseSchema.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XercesAttGroupInfo.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XercesElementWildcard.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XercesGroupInfo.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XMLSchemaDescriptionImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XSDDOMParser.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XSDErrorReporter.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XSDLocator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/XUtil.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/FieldActivator.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/FieldValueMap.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/IC_Field.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/IC_Key.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/IC_KeyRef.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/IC_Selector.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/IC_Unique.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/IdentityConstraint.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/IdentityConstraintHandler.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/ValueStore.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/ValueStoreCache.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/XercesXPath.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/XPathMatcher.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/XPathMatcherStack.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/validators/schema/identity/XPathSymbols.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/sax2/sax2Dummy.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/DOMException.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/DOMLSException.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/DOMRangeException.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/DOMXPathException.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMAttrImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMAttrMapImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMAttrNSImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMCDATASectionImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMCharacterDataImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMChildNode.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMCommentImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMConfigurationImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMDeepNodeListImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMDocumentFragmentImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMDocumentImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMDocumentTypeImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMElementImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMElementNSImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMEntityImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMEntityReferenceImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMErrorImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMImplementationImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMImplementationListImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMImplementationRegistry.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMLocatorImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMLSInputImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMLSOutputImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMLSSerializerImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNamedNodeMapImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNodeIDMap.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNodeImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNodeIteratorImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNodeListImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNodeVector.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNormalizer.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMNotationImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMParentNode.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMProcessingInstructionImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMRangeImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMStringListImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMStringPool.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMTextImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMTreeWalkerImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMTypeInfoImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMXPathExpressionImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMXPathNSResolverImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/DOMXPathResultImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/XSDElementNSImpl.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/xinclude/XIncludeDOMDocumentProcessor.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/xinclude/XIncludeLocation.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/xinclude/XIncludeUtils.cpp"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "3.1.1/xerces-c-3.1.1/src"
                ]
            },

            "conditions": [
                ["OS=='win'", {
                    "defines": [
                        # these are from vcproj:
                        "WIN32",
                        "_WINDOWS",
                        "_CRT_SECURE_NO_DEPRECATE",
                        "XERCES_STATIC_LIBRARY",
                        "XERCES_USE_TRANSCODER_WINDOWS",
                        "XERCES_USE_MSGLOADER_INMEMORY",
                        "XERCES_USE_NETACCESSOR_WINSOCK",
                        "XERCES_USE_FILEMGR_WINDOWS",
                        "XERCES_USE_MUTEXMGR_WINDOWS",
                        "XERCES_PATH_DELIMITER_BACKSLASH",
                        "HAVE_STRICMP",
                        "HAVE_STRNICMP",
                        "HAVE_LIMITS_H",
                        "HAVE_SYS_TIMEB_H",
                        "HAVE_FTIME",
                        "HAVE_WCSUPR",
                        "HAVE_WCSLWR",
                        "HAVE_WCSICMP",
                        "HAVE_WCSNICMP"
                    ],
                    "sources": [
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/FileManagers/WindowsFileMgr.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/MutexManagers/WindowsMutexMgr.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/WinSock/BinHTTPURLInputStream.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/WinSock/WinSockNetAccessor.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/Transcoders/Win32/Win32TransService.cpp"
                    ],
                    "link_settings": {
                        "libraries": [
                            "-ladvapi32.lib"
                        ]
                    },
                    "direct_dependent_settings": {
                        "defines": [
                            "XERCES_STATIC_LIBRARY" # declspec(dllimport)
                        ]
                    }
                }],

                ["OS=='mac'", {
                    "defines": [
                        "HAVE_CONFIG_H"
                    ],
                    "sources": [
						"3.1.1/xerces-c-3.1.1/src/stricmp.c",
						"3.1.1/xerces-c-3.1.1/src/strnicmp.c",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/FileManagers/PosixFileMgr.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/MutexManagers/PosixMutexMgr.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Curl/CurlNetAccessor.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Curl/CurlURLInputStream.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/Transcoders/MacOSUnicodeConverter/MacOSUnicodeConverter.cpp"
                    ],
                    "direct_dependent_settings": {
					"xcode_settings": {
                		"OTHER_LDFLAGS" : [ "-lpthread", 
                			  				"-lcurl", 
                							"-framework CoreFoundation", 
                							"-framework CoreServices" 
                				  			]
          			  }
                    }
                }],
                ["OS=='iOS'", {
                    "defines": [
                        "HAVE_CONFIG_H"
                    ],
                    "sources": [
						"3.1.1/xerces-c-3.1.1/src/stricmp.c",
						"3.1.1/xerces-c-3.1.1/src/strnicmp.c",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/FileManagers/PosixFileMgr.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/MutexManagers/NoThreadMutexMgr.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Socket/SocketNetAccessor.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Socket/UnixHTTPURLInputStream.cpp",
						"3.1.1/xerces-c-3.1.1/src/xercesc/util/Transcoders/Iconv/IconvTransService.cpp"
                    ],
                    "direct_dependent_settings": {
					"xcode_settings": {
                		"OTHER_LDFLAGS" : [ "-lpthread", 
                			  				"-lcurl", 
                							"-framework CoreFoundation" 
                				  			]
          			  }
                    }
                }],


                ["OS=='linux'", {
                    "defines": [
                        "HAVE_CONFIG_H"
                    ],
                    "sources": [
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/FileManagers/PosixFileMgr.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/MutexManagers/PosixMutexMgr.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Curl/CurlNetAccessor.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Curl/CurlURLInputStream.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Socket/SocketNetAccessor.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Socket/UnixHTTPURLInputStream.cpp",
                        "3.1.1/xerces-c-3.1.1/src/xercesc/util/Transcoders/IconvGNU/IconvGNUTransService.cpp",
                        "3.1.1/xerces-c-3.1.1/src/stricmp.c",
                        "3.1.1/xerces-c-3.1.1/src/strnicmp.c",
                        "3.1.1/xerces-c-3.1.1/src/towlower.c",
                        "3.1.1/xerces-c-3.1.1/src/towupper.c"
                    ],
                    "link_settings": {
                        "libraries": [
                            "-lpthread",
                            "-lcurl",
                            "-lnsl"
                        ]
                    }
                }]
            ]
        },
        {
            "target_name": "xerces_sample_PParse",
            "type": "executable",
            "test" : {
                "cwd": "3.1.1/xerces-c-3.1.1/samples",
                "args": [ "data/personal.xml" ]
            },
            "sources": [ "3.1.1/xerces-c-3.1.1/samples/src/PParse/PParse.cpp",
            			 "3.1.1/xerces-c-3.1.1/samples/src/PParse/PParseHandlers.cpp"
             ],
            "dependencies": [
                "xerces"
            ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ],
                ["OS=='mac'",
                    {
                        "type": "none"
                    }
                ]
            ]
        }
    ]
}
