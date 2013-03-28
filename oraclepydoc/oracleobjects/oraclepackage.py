from oracleplsqlsource import OraclePLSQLSource


class OraclePackage:

    def __init__(self, name, all_arguments, all_return_values, definition_source, body_source):
        #debug_message("debug: generating plsql package %s" % name)
        self.name = name
        self.source = OraclePLSQLSource(definition_source)
        self.body_source = None
        if body_source:
            self.body_source = OraclePLSQLSource(body_source)

    def getXML(self):
        """get package metadata"""
        xml_text = '''<package id="package-%s">
                        <name>%s</name>
                        <declaration>%s</declaration>
                        <body>%s</body>
                      </package>''' % ( self.name, self.name, self.source.getXML(), self.body_source.getXML())
        return xml_text
