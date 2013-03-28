class OracleTypeAttribute:
    """Type attribute object"""

    def __init__(self, name, type_mod, type_owner, type_name, length, precision, \
                 scale, character_set_name):
        self.__name = name
        self.__type = type_name
        self.__type_mod = type_mod
        self.__type_owner = type_owner
        self.__length = length
        self.__precision = precision
        self.__scale = scale
        self.__character_set_name = character_set_name

    def getName(self):
        """Get attribute name"""
        return self.__name

    def getType(self):
        """Get type of the attribute"""
        return self.__type

    def getTypeModifier(self):
        """Type modifier of the attribute"""
        return self.__type_mod

    def getTypeOwner(self):
        """Get owner of attribute type"""
        return self.__type_owner

    def getLength(self):
        """Get type length of the attribute"""
        return self.__length

    def getPrettyType(self):
        """Get pretty formated type in the form of type(x,y)"""
        type_len = self.__type
        if self.__length is not None:
            type_len = '(%s)' % self.__length
        elif self.__precision is not None:
            if self.__scale is not None:
                type_len = '(%s,%s)' % (self.__precision, self.__scale)
            else:
                type_len = '(%s)' % self.__precision
        return type_len

    def getPrecision(self):
        """Get type precision of the attribute"""
        return self.__precision

    def getScale(self):
        """Get type scale of the attribute"""
        return self.__scale

    def getCharSetName(self):
        """Get character set name of the attribute"""
        return self.__character_set_name
