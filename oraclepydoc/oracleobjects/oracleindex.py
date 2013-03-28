class OracleIndex:

    def __init__(self, name, data_dict):
        self.name = name
        table_name, type, uniqueness, include_column, generated, secondary = data_dict.all_indexes[name]
        self.table_name = table_name
        self.type = type
        self.uniqueness = uniqueness
        self.include_column = include_column
        self.generated = generated
        self.secondary = secondary

        self.columns = {}
        if data_dict.all_index_columns.has_key(name):
            for table_name, column , position in data_dict.all_index_columns[name]:
                self.columns[position] = column
        if data_dict.all_index_expressions.has_key(name):
            for table_name, expression , position in data_dict.all_index_expressions[name]:
                self.columns[position] = expression


    def getXML(self):
        """get data about index in xml"""
        xml_text = '''<index id="index-%s">
                        <name>%s</name>
                        <type>%s</type>
                        <table>table-%s</table>
                        <uniqueness>%s</uniqueness>
                        <generated>%s</generated>
                        <secondary>%s</secondary>''' % ( self.name, self.name, self.type, self.table_name,
                                                        self.uniqueness, self.generated, self.secondary)

        xml_text += '<ind_columns>'
        for position in self.columns.keys():
            xml_text += '<column>column-%s</column>' % self.columns[position]
        xml_text += '</ind_columns></index>'
        return xml_text
