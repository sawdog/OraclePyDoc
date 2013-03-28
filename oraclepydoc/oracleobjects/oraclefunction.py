from oracleprocedure import OracleProcedure


class OracleFunction(OracleProcedure):

    def __init__(self, name, arguments, return_data_type, source = None):
        #debug_message("debug: generating plsql function %s" % name)
        OracleProcedure.__init__(self, name, arguments, source)
        self.return_data_type = ''
        if return_data_type:
            self.return_data_type = return_data_type

    def getXML(self):
        """get function metadata"""
        xml_text = '''<function id="procedure-%s">
                        <name>%s</name>
                        <returns>%s</returns>
                        <source>%s</source>''' % (self.name, self.name, self.return_data_type,
                                                              self.source.getXML())
        if self.arguments:
            xml_text += '<arguments>'
            for argument in self.arguments:
                xml_text += argument.getXML()
            xml_text += '</arguments>'

        xml_text += '</function>'
        return xml_text
