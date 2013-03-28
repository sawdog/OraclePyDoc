class OracleColumn:
    """! \brief Oracle column represents table column object"""

    def __init__(self, name, column_id, data_type, nullable, data_default, comments):
        self.column_id = column_id
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.data_default = data_default
        self.comments = comments

    def getXML(self, table_name):
        """! \brief get xml representation of column"""
        #TODO: and it sucks to pass table_name via getXML, fix it
        return '''<column id="column-%s.%s">
                    <name>%s</name>
                    <position>%s</position>
                    <datatype>%s</datatype>
                    <default_value>%s</default_value>
                    <nullable>%s</nullable>
                    <comments><![CDATA[%s]]></comments>
                  </column>\n''' % (table_name, self.name,
                    self.name, self.column_id, self.data_type,
                    self.data_default, self.nullable,
                    self.comments)

