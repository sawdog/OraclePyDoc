from oraclecolumn import OracleColumn


class OracleViewColumn(OracleColumn):

    def __init__(self, name, column_id, data_type, nullable, data_default, comments, table_name, data_dict):
        #debug_message("debug: generating view column %s" % name)
        OracleColumn.__init__(self, name, column_id, data_type, nullable, data_default, comments)
        # check due the e.g. count(*) columns...
        try:
            self.insertable, self.updatable, self.deletable = data_dict.all_updatable_columns[table_name, name]
        except KeyError:
            self.insertable = self.updatable = self.deletable = 'n/a'

    def getXML(self, table_name):
        """get xml representation of column"""
        #TODO: and it sucks to pass table_name via getXML, fix it
        return '''<column id="column-%s.%s">
                    <name>%s</name>
                    <position>%s</position>
                    <datatype>%s</datatype>
                    <default_value>%s</default_value>
                    <nullable>%s</nullable>
                    <comments><![CDATA[%s]]></comments>
                    <insertable>%s</insertable>
                    <updatable>%s</updatable>
                    <deletable>%s</deletable>
                  </column>\n''' % (table_name, self.name,
                    self.name, self.column_id , self.data_type,
                    self.data_default , self.nullable,
                    self.comments, self.insertable, self.updatable, self.deletable)
