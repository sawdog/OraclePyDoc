class OracleProcedureArgument:
    def __init__(self, name, data_type, default_value, in_out ):
        #debug_message("debug: generating plsql argument %s" % name)
        self.name = name
        self.data_type = data_type
        self.default_value = default_value
        self.in_out = in_out

    def getXML(self):
        """get argument metadata in xml"""
        return '''<argument>
                    <name>%s</name>
                    <data_type>%s</data_type>
                    <default_value>%s</default_value>
                    <in_out>%s</in_out>
                  </argument>''' % (self.name, self.data_type, self.default_value, self.in_out)
