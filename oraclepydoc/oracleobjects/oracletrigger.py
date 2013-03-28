from oracletriggercolumn import OracleTriggerColumn

class OracleTrigger:

    def __init__(self, name, data_dict):
        #debug_message("debug: generating trigger %s" % name)
        self.name, self.type, self.event, self.base_object_type, self.table_name, self.nested_column_name, \
                   self.referencing_names, self.when_clause, self.status, self.description, self.action_type,\
                   self.body = data_dict.all_triggers[name]
        # initalize trigger columns
        self.columns = []
        if data_dict.all_trigger_columns.has_key(self.name):
            for name, table_name, column_name, column_list, column_usage in data_dict.all_trigger_columns[self.name]:
                self.columns.append(OracleTriggerColumn(column_name, column_list, column_usage))


    def getXML(self):
        code_text = 'CREATE TRIGGER %s\n' % self.description
        code_text += self.referencing_names + '\n'
        if self.when_clause:
            code_text += 'WHEN %s \n' % self.when_clause
        code_text += self.body

        xml_text = '''<trigger id="trigger-%s">
                        <name>%s</name>
                        <code><![CDATA[%s]]></code></trigger>''' % (self.name, self.name, code_text )
        return xml_text
