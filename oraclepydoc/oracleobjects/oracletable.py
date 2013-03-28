from oraclecolumn import OracleColumn
from oracleindex import OracleIndex
from oracletrigger import OracleTrigger
from oracleuniqueconstraint import OracleUniqueConstraint
from oraclecheckconstraint import OracleCheckConstraint
from oracletabpartition import OracleTabPartition
from oraclereferentialconstraint import OracleReferentialConstraint


class OracleTable:

    def __init__(self, name, data_dict):
        #debug_message('debug: creating table object %s' % name)
        # TODO delete old crap below
        self.name = name
        self.partitioned, self.secondary, self.index_organized, \
            self.clustered, self.cluster_name, self.nested, \
            self.temporary, self.tablespace_name = data_dict.all_tables[name]

        self.comments = data_dict.all_table_comments.get(name)
        self.columns = self._get_columns(data_dict)

        self.primary_key             = self._get_primary_key(name, data_dict)
        self.unique_keys             = self._get_unique_keys(name, data_dict)
        self.check_constraints       = self._get_check_constraints(name, data_dict)
        self.referential_constraints = self._get_ref_constraints(name, data_dict)
        self.indexes                 = self._get_indexes(name, data_dict)
        self.triggers                = self._get_triggers(data_dict)

        self.tab_partitions          = self._get_tab_partitions(name, data_dict)
        self.referenced_by = None
        if data_dict.table_referenced_by.has_key(name):
            self.referenced_by       = data_dict.table_referenced_by[name]


    def _get_primary_key(self, table_name, data_dict):
        _primary_key_name = data_dict.table_primary_key_map.get(table_name)
        primary_key = None
        if _primary_key_name:
            #debug_message('debug: generating primary key %s' % _primary_key_name)
            primary_key = OracleUniqueConstraint(_primary_key_name, data_dict)
        return primary_key

    def _get_unique_keys(self, table_name, data_dict):
        #debug_message('debug: generating unique keys')
        unique_keys = []
        t = data_dict.table_unique_key_map.get(table_name)
        if not t:
            return None
        for key_name in t:
            #debug_message('debug: generating unique key %s' % key_name )
            unique_key = OracleUniqueConstraint(key_name, data_dict)
            unique_keys.append(unique_key)
        return unique_keys

    def _get_check_constraints(self, table_name, data_dict):
        #debug_message('debug: generating check constraints')
        check_constraints = []
        t = data_dict.table_check_constraint_map.get(table_name)
        if not t:
            return None
        for constraint_name in t:
            #debug_message('debug: generating check constraint %s' % constraint_name)
            constraint = OracleCheckConstraint(constraint_name, data_dict)
            check_constraints.append(constraint)
        return check_constraints

    def _get_ref_constraints(self, table_name, data_dict):
        #debug_message('debug: generating foreign key constraints')
        referential_constraints = []
        t = data_dict.table_foreign_key_map.get(table_name)
        if not t:
            return None
        for constraint_name in t:
            #debug_message('debug: generating foreign key %s' % constraint_name)
            constraint = OracleReferentialConstraint(constraint_name, data_dict)
            referential_constraints.append(constraint)
        return referential_constraints


    def _get_tab_partitions(self, name, data_dict):
        #debug_message('debug: generating partitions')
        partitions = []
        if not data_dict.all_tab_partitions.has_key(self.name):
            #debug_message('debug: no partitons found')
            return []
        for partition_position, partition_name, tablespace_name, high_value in data_dict.all_tab_partitions[self.name]:
            partitions.append(OracleTabPartition(partition_position, partition_name, tablespace_name, high_value))
        return partitions


    def _get_columns(self, data_dict):
        #debug_message('debug: generating columns')
        columns = {}
        # Fixme: need proper hadling iot overflow segment columns
        if data_dict.all_columns.has_key(self.name):
            for column, data_type, nullable, column_id, data_default in data_dict.all_columns[self.name]:
                #debug_message('debug: generating column %s' % column)
                if data_dict.all_col_comments.has_key((self.name, column)):
                    comments = data_dict.all_col_comments[self.name, column]
                else:
                    comments = ''
                columns[column_id] = OracleColumn(column, column_id, data_type, nullable, data_default, comments)
        return columns


    def _get_indexes(self, table_name, data_dict):
        #debug_message('debug: generating indexes')
        indexes = []
        if  data_dict.table_index_map.has_key(table_name):
            for index_name in data_dict.table_index_map[table_name]:
                #debug_message('debug: generating index %s' % index_name)
                index = OracleIndex(index_name, data_dict)
                indexes.append(index)
        return indexes

    def _get_triggers(self, data_dict):
        #debug_message('debug: generating triggers')
        triggers = []
        if  data_dict.table_trigger_map.has_key(self.name):
            for trigger_name in data_dict.table_trigger_map[self.name]:
                #debug_message('debug: generating trigger %s' % trigger_name)
                triggers.append(OracleTrigger(trigger_name, data_dict))
        return triggers

    def getXML(self):
        """get xml represention of table"""
        xml_text = '''<table id="table-%s">
                         <name>%s</name>
                         <index_orginized>%s</index_orginized>
                         <tablespace>%s</tablespace>
                         <partitioned>%s</partitioned>
                         <temporary>%s</temporary>
                         <nested>%s</nested>
                         <clustered>%s</clustered>
                         <cluster_name>%s</cluster_name>
                         <secondary>%s</secondary>
                         <comments><![CDATA[%s]]></comments>
                         ''' % (self.name,
                                self.name,
                                self.index_organized,
                                self.tablespace_name,
                                self.partitioned,
                                self.temporary,
                                self.nested,
                                self.clustered,
                                self.cluster_name,
                                self.secondary,
                                self.comments)
        xml_text += '<columns>'
        #xml for table columns
        for position in self.columns.keys():
            xml_text += self.columns[position].getXML(self.name)
        xml_text += '</columns>\n'
        xml_text += '<constraints>\n'
        if self.primary_key:
            xml_text +=  self.primary_key.getXML()
        if self.unique_keys:
            for unique_key in self.unique_keys:
                xml_text += unique_key.getXML()
        if self.check_constraints:
            for constraint in self.check_constraints:
                xml_text += constraint.getXML()
        if self.referential_constraints:
            for constraint in self.referential_constraints:
                xml_text += constraint.getXML()
        xml_text += '</constraints>\n'
        if self.indexes:
            xml_text += '<indexes>\n'
            for index in self.indexes:
                xml_text += index.getXML()
            xml_text += '</indexes>'
        if self.triggers:
            xml_text += '<triggers>'
            for trigger in self.triggers:
                xml_text += trigger.getXML()
            xml_text += '</triggers>'
        if self.referenced_by:
            xml_text += '<references>'
            for name in self.referenced_by:
                xml_text += '<reference><table>table-%s</table><constraint>constraint-%s</constraint></reference>' % name
            xml_text += '</references>'
        xml_text += '</table>\n'
        return xml_text
