class OracleTypeMethod:
    """Represents Oracle Type methods"""
    def __init__(self, name, method_type, param_count, results_count):
        self.__name = name
        self.__type = method_type
        self.__results_count = results_count
        self.__param_count = param_count

    def getName(self):
        """Get type method name"""
        return self.__name

    def getType(self):
        """Get method type"""
        return self.__type

    def getResultsCount(self):
        """Get count of results returned by the method"""
        return self.__results_count

    def getParametersCount(self):
        """Get count of method parameters"""
        return self.__param_count
