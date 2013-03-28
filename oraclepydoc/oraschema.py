""" OraSchemaDataDictionary class queries data from Oracle Data Dictionary """

import os.path

from oracleobjects.oracletable import OracleTable
from oracleobjects.oracleindex import OracleIndex
from oracleobjects.oracleuniqueconstraint import OracleUniqueConstraint
from oracleobjects.oracleview import OracleView
from oracleobjects.oracletrigger import OracleTrigger
from oracleobjects.oracleprocedure import OracleProcedure
from oracleobjects.oraclefunction import OracleFunction
from oracleobjects.oraclepackage import OraclePackage
from oracleobjects.oraclejavasource import OracleJavaSource
from oracleobjects.oraclecheckconstraint import OracleCheckConstraint
from oracleobjects.oraclesequence import OracleSequence
from oracleobjects.oraclemview import OracleMView
from oracleobjects.oraclereferentialconstraint import \
        OracleReferentialConstraint
from oracleobjects.oraclejob import OracleJob

from oraddlsource import OraDDLSource

from oraverbose import debug_message
from oraverbose import set_verbose_mode


class OracleSchema(object):

    def __init__(self, cfg):
        self.ddlSource = OraDDLSource(cfg)
        set_verbose_mode(cfg.verbose_mode)
        self.packageBodies = cfg.pb
        self.tables = self._get_all_tables(cfg.dictionary)
        self.indexes = self._get_all_indexes(cfg.dictionary)
        self.constraints = self._get_all_constraints(cfg.dictionary)
        self.views = self._get_all_views(cfg.dictionary)
        self.mviews = self._get_all_mviews(cfg.dictionary)
        self.triggers = self._get_all_table_triggers(cfg.dictionary)
        self.procedures = self._get_all_procedures(cfg.dictionary)
        self.functions = self._get_all_functions(cfg.dictionary)
        self.packages = self._get_all_packages(cfg.dictionary)
        self.sequences = self._get_all_sequences(cfg.dictionary)
        self.java_sources = self._get_all_java_sources(cfg.dictionary)
        self.jobs = self._get_all_jobs(cfg.dictionary)
        self.dependencies = cfg.dictionary.dependencies
        # TODO: why i need that name?
        # Until we access multiple schemas during a single process, the schema
        # is also the cfg.currentUser; this is being used to create links
        # in dependencies, where the schema needs to be known to properly
        # the link.
        self.name = cfg.currentUser


    def getXML(self):
        """get xml representaion of given schema"""
        xml_text = ['<schema>']
        for table in self.tables:
            xml_text.append(table.getXML())

        for view in self.views:
            xml_text.append(view.getXML())

        for mview in self.mviews:
            xml_text.append(mview.getXML())

        for sequence in self.sequences:
            xml_text.append(sequence.getXML())

        for procedure in self.procedures:
            xml_text.append(procedure.getXML())

        for function in self.functions:
            xml_text.append(function.getXML())

        for package in self.packages:
            xml_text.append(package.getXML())

        for job in self.jobs:
            xml_text.append(job.getXml())

        xml_text.append('</schema>')
        return '\n'.join(xml_text)


    def _get_all_tables(self, data_dict):
        tables = []
        debug_message('generating tables')
        for table_name in data_dict.all_table_names:
            tables.append(OracleTable(table_name, data_dict))
            self.ddlSource.getDDLScript('TABLE', table_name)
        return tables

    def _get_all_indexes(self, data_dict):
        debug_message('generating indexes')
        indexes = []
        for index_name in data_dict.all_index_names:
            indexes.append(OracleIndex(index_name, data_dict))
            self.ddlSource.getDDLScript('INDEX', index_name)
        return indexes

    def _get_all_constraints(self, data_dict):
        debug_message('generating constraints')
        constraints = []
        for name in data_dict.all_constraint_names:
             table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
             if type in ("P", "U"):
                 constraints.append(OracleUniqueConstraint(name, data_dict))
             elif type == "R":
                 constraints.append(OracleReferentialConstraint(name, data_dict))
             elif type == "C":
                 constraints.append(OracleCheckConstraint(name, data_dict))
        return constraints

    def _get_all_views(self, data_dict):
        debug_message('generating views')
        views = []
        for view_name in data_dict.all_view_names:
            views.append(OracleView(view_name, data_dict))
            self.ddlSource.getDDLScript('VIEW', view_name)
        return views


    def _get_all_mviews(self, data_dict):
        debug_message('generating materialized views')
        mviews = []
        for mv_name in data_dict.all_mview_names:
            mviews.append(OracleMView(mv_name, data_dict))
            self.ddlSource.getDDLScript('MATERIALIZED_VIEW', mv_name)
        return mviews


    def _get_all_table_triggers(self, data_dict):
        debug_message('generating triggers')
        triggers = []
        for trigger_name in data_dict.table_triggers:
            triggers.append(OracleTrigger(trigger_name, data_dict))
            self.ddlSource.getDDLScript('TRIGGER', trigger_name)
        return triggers

    def _get_all_procedures(self, data_dict):
        debug_message('generating procedures')
        procedures = []
        for name in data_dict.all_procedure_names:
            procedure = OracleProcedure(name, data_dict.proc_arguments.get(name, None), \
                                        data_dict.all_procedures.get(name, None))
            procedures.append(procedure)
            self.ddlSource.getDDLScript('PROCEDURE', name)
        return procedures

    def _get_all_java_sources(self, data_dict):
        debug_message('generating java sources')
        java_sources = []
        for name in data_dict.all_java_source_names:
            java_source = OracleJavaSource(name,data_dict.all_java_sources.get(name, None))
            java_sources.append(java_source)
        return java_sources

    def _get_all_functions(self, data_dict):
        debug_message('generating functions')
        functions = []
        for name in data_dict.all_function_names:
            function = OracleFunction(name, data_dict.proc_arguments.get(name, None), \
                                      data_dict.func_return_arguments.get(name, None),\
                                      data_dict.all_functions.get(name, None))
            functions.append(function)
            self.ddlSource.getDDLScript('FUNCTION', name)
        return functions

    def _get_all_packages(self, data_dict):
        debug_message('generating packages')
        packages = []
        for name in data_dict.all_package_names:
            all_arguments = data_dict.package_arguments.get(name, None)
            all_return_values = data_dict.package_return_values.get(name, None)
            def_source = data_dict.all_packages[name]
            if self.packageBodies == True:
                body_source = data_dict.all_package_bodies.get(name, None)
            else:
                body_source = {0: 'Source code generator disabled'}
            package = OraclePackage(name, all_arguments, all_return_values, def_source, body_source)
            packages.append(package)
            self.ddlSource.getDDLScript('PACKAGE', name)
            self.ddlSource.getDDLScript('PACKAGE_BODY', name)
        return packages

    def _get_all_sequences(self, data_dict):
        debug_message('generating sequences')
        sequences = []
        for name in data_dict.sequence_names:
            min_value, max_value, step, cycled, ordered, cache_size = data_dict.sequences[name]
            seq = OracleSequence(name, min_value, max_value, step, cycled, ordered, cache_size)
            sequences.append(seq)
            self.ddlSource.getDDLScript('SEQUENCE', name)
        return sequences


    def _get_all_jobs(self, data):
        debug_message('generating jobs')
        jobs = []
        for job, log_user, priv_user, schema_user, total_time, broken, interval, failures, what in data.jobs:
            jobs.append(OracleJob(job, log_user, priv_user, schema_user, total_time, broken, interval, failures, what))
        return jobs



if __name__ == '__main__':
    import cx_Oracle
    import orasdict
    from osdconfig import OSDConfig
    #connection = cx_Oracle.connect('s0/asgaard')
    cfg = OSDConfig()
    cfg.connection = cx_Oracle.connect('s0/asgaard')
    cfg.dictionary = orasdict.OraSchemaDataDictionary(cfg)
    schema = OracleSchema(cfg)

