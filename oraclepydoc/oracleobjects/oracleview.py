from oracleviewcolumn import OracleViewColumn
from oracletrigger import OracleTrigger
from oracleviewconstraint import OracleViewConstraint


class OracleView:

    def __init__(self, name, data_dict):
        #debug_message("debug: generating view %s" % name)
        self.name = name
        self.text = data_dict.all_views[name]
        self.columns = self._get_columns(data_dict)
        self.constraints = self._get_constraints(data_dict)
        self.comments = data_dict.all_table_comments.get(name)
        self.triggers = self._get_triggers(data_dict)


    def getXML(self):
        """get data about view in xml"""
        xml_text = '''<view id="view-%s">
                        <name>%s</name>
                        <comments><![CDATA[%s]]></comments>
                        <query_text><![CDATA[%s]]></query_text>''' % (
                    self.name, self.name, self.comments, self.text)
        if self.columns:
            xml_text += '<columns>\n'
            for position in self.columns.keys():
                xml_text += self.columns[position].getXML(self.name)
            xml_text += '</columns>\n'

        if self.constraints:
            xml_text += '<constraints>'
            for constraint in self.constraints:
                xml_text += constraint.getXML()
            xml_text += '</constraints>'

        if self.triggers:
            xml_text += '<triggers>'
            for trigger in self.triggers:
                xml_text += trigger.getXML()
            xml_text += '</triggers>'
        xml_text += '</view>'
        return xml_text


    def _get_columns(self, data_dict):
        columns = {}
        for column, data_type, nullable, column_id, data_default in data_dict.all_columns[self.name]:
            if data_dict.all_col_comments.has_key((self.name, column)):
                comments = data_dict.all_col_comments[self.name, column]
            else:
                comments = ''
            columns[column_id] = OracleViewColumn(column, column_id, data_type, nullable, data_default, comments, self.name, data_dict)
        return columns

    def _get_constraints(self, data_dict):
        constraints = []
        t = data_dict.view_constraint_map.get(self.name)
        if not t:
            return None
        for constraint_name in t:
            constraint = OracleViewConstraint(constraint_name, data_dict)
            constraints.append(constraint)
        return constraints

    def _get_triggers(self, data_dict):
        triggers = []
        if  data_dict.table_trigger_map.has_key(self.name):
            for trigger_name in data_dict.table_trigger_map[self.name]:
                triggers.append(OracleTrigger(trigger_name, data_dict))
        return triggers
