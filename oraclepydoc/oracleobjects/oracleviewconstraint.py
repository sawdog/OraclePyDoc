class OracleViewConstraint:

    def __init__(self, name, data_dict):
        #debug_message("debug: generating view constraint %s" % name)
        self.name = name
        self.table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
        if type == 'O':
            self.type = "With read only on view"
            self.columns = []
        else:
            self.type = "With check option on view"
            self.columns = {}
            for table_name, column_name, position in data_dict.all_constraited_columns.get(name, []):
                self.columns[position]=column_name
        self.check_cond = check_cond

    def getXML(self):
        """get constraint metadata in xml"""
        xml_text = '''<constraint id="constraint-%s">
                    <name>%s</name>
                    <type>%s</type>'''
        if self.columns:
            xml_text += '<columns>'
            for position in self.columns.keys():
                xml_text += '<column>name</column>'
            xml_text += '</columns>'
        xml_text += '</constraint>'
        return xml_text
