from oracleplsqlsource import OraclePLSQLSource


class OracleJavaSource(OraclePLSQLSource):
    def __init__(self, name, source):
        self.name = name
        #debug_message("debug: generating java source ")
        OraclePLSQLSource.__init__(self,source)
