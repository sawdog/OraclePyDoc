class OracleCheckConstraint:

    def __init__(self, name, data_dict):
        self.name = name
        self.table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
        self.type = "Check"
        self.check_cond = check_cond
        self.columns = {}
        for table_name, column_name, position in data_dict.all_constraited_columns[name]:
            self.columns[position]=column_name
        # TODO all above should be deleted
        self.__name = name
        self.__table_name = table_name
        self.__type = "Check"
        self.__check_cond = check_cond
        self.__columns = self.columns

    def getName(self):
        return self.__name

    def getCheckCondition(self):
        return self.__check_cond

    def getXML(self):
        '''get xml for check constraint'''
        xml_text = '''<constraint id="constraint-%s" type="check">
                      <name>%s</name>
                      <check_condition><![CDATA[%s]]></check_condition>''' % (
                                                          self.__name, self.__name, self.__check_cond)
        xml_text += '</constraint>\n'
        return xml_text
