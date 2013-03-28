class OracleType:
    """Represents Oracle Object type"""

    def __init__(self, name, typecode, predefined, incomplete,
                 type_oid, attributes_count,
                 methods_count):
        self.__name = name
        self.__typecode = typecode
        self.__predefined = predefined
        self.__incomplete = incomplete
        self.__source = None
        self.__body_source = None
        self.__type_oid = type_oid
        self.__attrubutes_count = attributes_count
        self.__methods_count = methods_count

    def setDeclarationSource(self, source):
        """Set type declaration source code text"""
        self.__source = source

    def setImplementationSource(self, source):
        """Set Type implementation source code text"""
        self.__body_source = source

    def getName(self):
        """Get type name"""
        return self.__name

    def getTypeCode(self):
        """Get type typecode"""
        return self.__typecode

    def isPredefined(self):
        """Indicates whether the type is a predefined type"""
        return self.__predefined == 'YES'

    def isIncomplete(self):
        """Indicates whether the type is an incomplete type"""
        return self.__incomplete == 'YES'

    def getDeclarationSource(self):
        """Get type declaration source code"""
        return self.__source

    def getImplementationSource(self):
        """Get implementation source code"""
        return self.__body_source

    def getTypeOID(self):
        """Get object identifier (OID) of type"""
        return self.__type_oid

    def getMethodsCount(self):
        """Get count of methods in the type"""
        return self.__methods_count

    def getAttributesCount(self):
        """Get count of attributes in the type"""
        return self.__attrubutes_count
