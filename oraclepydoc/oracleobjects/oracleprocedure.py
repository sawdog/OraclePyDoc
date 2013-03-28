from oracleplsqlsource import OraclePLSQLSource
from oracleprocedureargument import OracleProcedureArgument


class OracleProcedure:

    def __init__(self, name, arguments, source = None):
        #debug_message("debug: generating plsql procedure %s" % name)
        self.name = name
        self.arguments = []
        self.source = None

        if arguments:
            arg_keys = arguments.keys()
            arg_keys.sort()
            for key in arg_keys:
                name, data_type, default_value, in_out = arguments[key]
                argument = OracleProcedureArgument(name, data_type, default_value, in_out)
                self.arguments.append(argument)
        if source:
            self.source = OraclePLSQLSource(source)

    def getXML(self):
        """get procedure metadata"""
        xml_text = '''<procedure id="procedure-%s">
                        <name>%s</name>
                        <source>%s</source>''' % (self.name, self.name, self.source.getXML())
        if self.arguments:
            xml_text += '<arguments>'
            for argument in self.arguments:
                xml_text += argument.getXML()
            xml_text += '</arguments>'

        xml_text += '</procedure>'
        return xml_text
