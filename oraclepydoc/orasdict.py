""" OraSchemaDataDictionary class queries data from Oracle Data Dictionary """

import fpformat
from oraverbose import debug_message
from oraclepydoc.oraverbose import set_verbose_mode

from oraschemasql import OracleCatalog


class OraSchemaDataDictionary:
    """! \brief Get all needed data from oracle data dictionary
       and initializes all attributes
    """

    def __init__(self, cfg):
        """! \param cfg a OSDConfig instance """

        self.cfg = cfg
        set_verbose_mode(cfg.verbose_mode)

        debug_message('Oracle server %s (TNS: %s)' % \
                    (cfg.connection.version, cfg.connection.tnsentry))

        # tables
        self.all_tables = self.__get_tables()
        self.all_table_names = self.all_tables.keys()
        self.all_table_names.sort()
        self.all_table_comments = self.__get_table_comments()
        self.all_tab_partitions = self.__get_tab_partitions()
        # columns
        self.all_columns = self.__get_columns()
        self.all_col_comments = self.__get_column_comments()
        # constraints
        self.all_constraints = self.__get_constraints()
        self.all_constraint_names = self.all_constraints.keys()
        self.all_constraint_names.sort()
        self.all_constraited_columns = self.__get_constraited_columns()
        # indexes
        self.all_indexes = self.__get_indexes()
        self.all_index_names = self.all_indexes.keys()
        self.all_index_names.sort()
        self.all_index_columns = self.__get_index_columns()
        self.all_index_expressions = self.__get_index_expressions()
        # views
        self.all_views = self.__get_views()
        self.all_view_names = self.all_views.keys()
        self.all_view_names.sort()
        self.all_updatable_columns = self.__get_updatable_columns()
        # materialized views (snapshots)
        self.all_mviews = self.__get_mviews()
        self.all_mview_names = self.all_mviews.keys()
        self.all_mview_names.sort()
        # table/view related mappings
        self.table_primary_key_map = {}
        self.table_unique_key_map = {}
        self.table_check_constraint_map = {}
        self.table_foreign_key_map = {}
        self.table_check_constraint_map = {}
        self.view_constraint_map = {}
        self.table_referenced_by = {}
        self.table_constraint_map= {}
        self.table_index_map = {}
        self.__set_table_maps()
        # triggers
        self.all_triggers = self.__get_triggers()
        self.all_trigger_names = self.all_triggers.keys()
        self.all_trigger_names.sort()
        self.all_trigger_columns = self.__get_trigger_columns()
        self.table_triggers = []
        self.table_trigger_map = {}
        self.schema_triggers = []
        self.__set_trigger_maps()
        # types
        self.types = self.__get_types()
        self.type_attributes = self.__get_type_attributes()
        self.type_methods = self.__get_type_methods()
        self.type_sources = {}
        self.type_body_sources = {}
        # pl/sql, java stuff
        self.all_functions = {}
        self.all_procedures = {}
        self.all_packages = {}
        self.all_package_bodies = {}
        self.all_java_sources = {}
        self.__set_user_sources()
        self.all_procedure_names = self.all_procedures.keys()
        self.all_procedure_names.sort()
        self.all_function_names = self.all_functions.keys()
        self.all_function_names.sort()
        self.all_package_names = self.all_packages.keys()
        self.all_package_names.sort()
        self.all_java_source_names = self.all_java_sources.keys()
        self.all_java_source_names.sort()
        # pl/sql arguments
        self.proc_arguments = {}
        self.func_return_arguments = {}
        self.package_arguments = {}
        self.package_return_values = {}
        self.__set_plsql_args()
        # sequences
        self.sequences = self.__get_sequences()
        self.sequence_names = self.sequences.keys()
        self.sequence_names.sort()
        # jobs
        self.jobs = self._getJobs()
        # dependencies
        # format { key : [ list of deps ] }
        self.dependencies = self.__getDependencies()


    def __set_table_maps(self):
        """Fill table_constraint_map, table_primary_key_map,
           table_check_constraint, table_foreign_key_map, table_index_map
        """
        # table_constraints
        for constraint_name in self.all_constraint_names:
            table_name = self.all_constraints[constraint_name][0]
            self.table_constraint_map.setdefault(table_name, []).\
                append(constraint_name)

        # uk, pk, fk, ck... constraint maps
        for constraint_name in self.all_constraint_names:
            table_name, type, check_cond, r_owner, r_constraint_name, \
            delete_rule = self.all_constraints[constraint_name]
            if type == 'P':
               self.table_primary_key_map[table_name] = constraint_name
            elif type == 'U':
                 self.table_unique_key_map.setdefault(table_name,[]).\
                     append(constraint_name)
            elif type == 'C':
                 self.table_check_constraint_map.setdefault(table_name,[]).\
                     append(constraint_name)
            elif type == 'R':
                 self.table_foreign_key_map.setdefault(table_name,[]).\
                     append(constraint_name)
                 # put row in table_referenced_by
                 _table_name = self.all_constraints[r_constraint_name][0]
                 self.table_referenced_by.setdefault(_table_name,[]).\
                     append((table_name, constraint_name))
            elif type in ('V','O'):
                 self.view_constraint_map.setdefault(table_name,[]).\
                     append(constraint_name)

        # table index map
        for index_name in self.all_index_names:
            table_name = self.all_indexes[index_name][0]
            self.table_index_map.setdefault(table_name,[]).append(index_name)


    def __set_trigger_maps(self):
        """Set table_triggers, table_trigger_map, schema_triggers"""
        for trigger_name in self.all_trigger_names:
            name, type, event, base_object_type, table_name, column_name, \
                referencing_names, when_clause, status, description, \
                action_type, body = self.all_triggers[trigger_name]
            if base_object_type in ('TABLE', 'VIEW'):
                self.table_triggers.append(trigger_name)
                self.table_trigger_map.setdefault(table_name,[]).append(name)
            elif base_object_type  == 'SCHEMA':
                self.schema_triggers.append(trigger_name)
        self.table_triggers.sort()


    def __set_user_sources(self):
        """Process users sources and put entries into appropriate structures"""
        for name, type, line, text in self.__get_user_source():
            if type == 'PROCEDURE':
                t = self.all_procedures.setdefault(name, {})
            elif type == 'FUNCTION':
                t = self.all_functions.setdefault(name, {})
            elif type == 'PACKAGE':
                t = self.all_packages.setdefault(name, {})
            elif type == 'PACKAGE BODY':
                t = self.all_package_bodies.setdefault(name, {})
            elif type == 'JAVA SOURCE':
                t = self.all_java_sources.setdefault(name, {})
            elif type == 'TYPE':
                t = self.type_sources.setdefault(name, {})
            elif type == 'TYPE BODY':
                t = self.type_body_sources.setdefault(name, {})
            else:
                continue
            t[int(float(line))] = text


    def __set_plsql_args(self):
        """Process pl/sql arguments"""
        all_arguments = self.__get_arguments()
        for name, package_name, argument_name, position, data_type, \
            default_value, in_out in all_arguments:
            if not package_name:
                if position:
                    t = self.proc_arguments.setdefault(name, {})
                    t[int(float(position))]= [argument_name, data_type, \
                                              default_value, in_out]
                else:
                    self.func_return_arguments[name] = data_type
            else:
                if float(position) > 0:
                    t = self.package_arguments.setdefault(package_name, {}).\
                      setdefault(name, {})
                    t[int(float(position))] =  argument_name, data_type, \
                     default_value, in_out
                else:
                    self.package_return_values.setdefault(package_name, {})[name]= data_type


    ################################################
    # INTERNAL FUNCTIONS FOR QUERY DATA DICTIONARY #
    ################################################

    def __get_tables(self):
        """Get tables"""
        # fix me with iot_table overflow segments
        #stmt = """select table_name, partitioned, secondary, cluster_name,
        #             iot_type, temporary,  nested, tablespace_name
        #          from user_tables"""
        stmt = self._prepareStatement(OracleCatalog['tables'])
        tables = {}
        print "get tables"
        for table, partitioned, secondary, cluster, iot_type, temporary, nested, tablespace_name in self.__query(stmt):
            debug_message('debug: table - %s' % table)
            _partitioned = 'No'
            _secondary = 'No'
            _index_organized = 'No'
            _clustered = 'No'
            _cluster_name = ''
            _nested = 'No'
            _temporary = 'No'
            _tablespace_name = tablespace_name
            if partitioned == 'YES':
                _partitioned = 'Yes'
            if secondary == 'Y':
                _secondary = 'Yes'
            if iot_type:
                _index_organized = 'Yes'
                _tablespace_name = '(IOT - see index tablespace)'
            if cluster:
                _clustered = 'Yes'
                _cluster_name = cluster
            if nested == 'Y':
                _nested = 'Yes'
            if temporary == 'Y':
                _temporary = 'Yes'
            tables[table] = _partitioned, _secondary, _index_organized, _clustered, _cluster_name, _nested,\
                            _temporary, _tablespace_name
        return tables


    def __get_tab_partitions(self):
        """ Search for available partitions.
        Returns a dictionary {tablename: [ [partition], [partition] ... ], tablename2: ... }
        It's something like grouping by tablename.
        """
#        stmt = '''select table_name, partition_name,
#                    tablespace_name, high_value,
#                    partition_position
#                    from user_tab_partitions order by table_name, partition_position'''
        stmt = self._prepareStatement(OracleCatalog['tab_partitions'])
        tab_partitions = {}
        print "get partitions"
        for table_name, partition_name, tablespace_name, high_value, partition_position in self.__query(stmt):
            aPart = [partition_position, partition_name, tablespace_name, high_value]
            if tab_partitions.has_key(table_name):
                tab_partitions[table_name].append(aPart)
            else:
                tab_partitions[table_name] = [aPart]
        return tab_partitions


    def __get_table_comments(self):
        """Get comments on tables and views"""
#        stmt = """SELECT table_name, comments
#            FROM user_tab_comments
#            WHERE comments is not null"""
        stmt = self._prepareStatement(OracleCatalog['tab_comments'])
        comments = {}
        print "get comments on tables and views"
        for table, comment in self.__query(stmt):
            debug_message('debug: comments on table - %s' % table)
            comments[table] = comment
        return comments


    def __get_column_comments(self):
        """Get all tables/views column comments"""
#        stmt = """ SELECT table_name, column_name, comments
#            FROM user_col_comments
#            where comments is not null"""
        stmt = self._prepareStatement(OracleCatalog['col_comments'])
        col_comments = {}
        print "get all tables/views column comments"
        for table, column, comment in self.__query(stmt):
            debug_message('debug: comments on table.column - %s.%s' % (table, column))
            col_comments[table,column] = comment
        return col_comments


    def __get_columns(self):
        """Get all columns for tables, views and clusters"""
#        stmt = """select table_name, column_name, data_type , data_length, data_precision,
#                         data_scale, nullable, column_id, data_default
#                    from user_tab_columns
#                    order by table_name, column_id"""
        stmt = self._prepareStatement(OracleCatalog['columns'])
        all_columns = {}
        print "get all columns for tables, views and clusters"
        for table, column, data_type, data_length, data_precision, data_scale, nullable, column_id, \
                data_default in self.__query(stmt):
            debug_message('debug:  table.column - %s.%s' % (table, column))
            _data_type = data_type
            t = all_columns.get(table, None)
            if not t:
                t = []
                all_columns[table] = t
            if data_type == 'NUMBER':
                if not data_precision:
                    data_precision = "38"
                _data_type = _data_type + '(%s' %data_precision
                if data_scale and data_scale <> 0:
                    _data_type = _data_type + ',%s' %data_scale
                _data_type = _data_type + ')'
            elif data_type in ('CHAR','VARCHAR2','NCHAR','NVARCHAR2','RAW','UROWID'):
                _data_type = _data_type + '(%s)' %data_length

            t.append((column, _data_type, nullable, column_id, data_default))
        return all_columns


    def __get_constraints(self):
        """get all_table/view constraints"""
#        stmt = """select  table_name, constraint_name, constraint_type, search_condition, r_owner,
#            r_constraint_name , delete_rule
#            from user_constraints where r_owner is null or r_owner = user"""
        stmt = self._prepareStatement(OracleCatalog['constraints'])
        cons ={}
        print  "get all table/view constraints"
        for table_name, name, type, check_cond, r_owner, r_constraint_name, delete_rule in self.__query(stmt):
            debug_message('debug: table.constraint - %s.%s' % (table_name, name))
            # take NN constraint only when it's allowed.
            # TODO: better way to get NN. Where clause in SQL statement above
            # is unpleasant as it's LONG type
            if type != 'C':
                cons[name]=(table_name, type, check_cond, r_owner, r_constraint_name, delete_rule)
            elif (not self.cfg.notNulls and check_cond.find(' IS NOT NULL') == -1) or self.cfg.notNulls:
                cons[name]=(table_name, type, check_cond, r_owner, r_constraint_name, delete_rule)
            else:
                if type != 'C':
                    print 'WARNING: skipped constraint %s (%s %s). Something is wrong propably.' % (name, check_cond, type)
        return cons


    def __get_constraited_columns(self):
        """Get all constrainted columns"""
#        stmt  = """select constraint_name, table_name, column_name, position from
#            user_cons_columns"""
        stmt = self._prepareStatement(OracleCatalog['cons_columns'])
        cs_cols = {}
        print  "get all constrainted columns"
        for name , table_name, column_name, position in self.__query(stmt):
            debug_message('debug: constrainted  table.column - %s.%s' % (table_name, column_name))
            t = cs_cols.get(name, None)
            if not t:
                t = []
                cs_cols[name] = t
            t.append( (table_name, column_name, position))
        return cs_cols;


    def __get_views(self):
        """Get all views"""
#        stmt = """ select view_name , text from user_views"""
        stmt = self._prepareStatement(OracleCatalog['views'])
        views = {}
        print "get all views"
        for name, text in self.__query(stmt):
            debug_message('debug: view - %s' % name)
            views[name]= text
        return views


    def __get_mviews(self):
        """ Get all materialized views """
        stmt = self._prepareStatement(OracleCatalog['mviews'])
        mviews = {}
        print 'get all materialized views'
        for name, container, query, updatable in self.__query(stmt):
            mviews[name] = container, query, updatable
        return mviews


    def __get_indexes(self):
        """Get all indexes"""
#        stmt = """select index_name, table_name, index_type, uniqueness, include_column, generated, secondary
#                    from user_indexes"""
        stmt = self._prepareStatement(OracleCatalog['indexes'])
        indexes = {}
        print "get all indexes"
        for name, table_name, type, uniqueness, include_column, generated, secondary in self.__query(stmt):
            debug_message('debug: index %s on table %s' % (name, table_name))
            indexes[name] = (table_name, type, uniqueness, include_column, generated, secondary)
        return indexes


    def __get_index_columns(self):
        """Get all index columns"""
#        |stmt = """select index_name, table_name, column_name, column_position from user_ind_columns"""
        stmt = self._prepareStatement(OracleCatalog['ind_columns'])
        ind_columns = {}
        print "get all index columns"
        for name, table_name, column_name, column_position in self.__query(stmt):
            debug_message('debug: column %s on index %s' % (column_name, name))
            t = ind_columns.get(name)
            if not t:
                t = []
                ind_columns[name] = t
            t.append(( table_name, column_name, column_position))

        return ind_columns


    def __get_index_expressions(self):
        """Get all index expressions"""
#        stmt = """select index_name, table_name, column_expression, column_position from user_ind_expressions"""
        stmt = self._prepareStatement(OracleCatalog['ind_expressions'])
        ind_expressions = {}
        print "get all index_expressions"
        for name, table_name, expression, position in self.__query(stmt):
            debug_message('debug: index expession on index %s' % name )
            t = ind_expressions.get(name)
            if not t:
                t = []
                ind_expressions[name] = t
            t.append((table_name, expression, position))

        return ind_expressions


    def __get_updatable_columns(self):
        """Get updatable columns on views"""
#        stmt = """select table_name, column_name, insertable, updatable, deletable
#            from all_updatable_columns
#            where table_name in (select view_name from user_views)"""
        stmt = self._prepareStatement(OracleCatalog['updatable_columns'])
        view_updatable_columns = {}
        print "get updatable columns"
        for table_name, column_name, insertable, updatable, deletable in self.__query(stmt):
            debug_message('debug: updatable column %s on view %s' % (column_name, table_name))
            view_updatable_columns[table_name, column_name] = (insertable, updatable, deletable)
        return view_updatable_columns


    def __get_triggers(self):
        """Get all triggers"""
#        stmt = """select trigger_name, trigger_type, triggering_event, base_object_type, table_name,
#            column_name, referencing_names, when_clause, status, description, action_type, trigger_body
#            from user_triggers"""
        stmt = self._prepareStatement(OracleCatalog['triggers'])
        triggers = {}
        print "get all triggers"
        for name, type, event, base_object_type, table_name, column_name, referencing_names, when_clause, status,\
            description, action_type, body in self.__query(stmt):
            debug_message('debug: trigger - %s' % name)
            triggers[name] = (name, type, event, base_object_type, table_name, column_name, referencing_names, \
                              when_clause, status, description, action_type, body)
        return triggers


    def __get_trigger_columns(self):
        """Get all trigger columns"""
#        stmt = "select trigger_name, table_name, column_name, column_list, column_usage from user_trigger_cols"
        stmt = self._prepareStatement(OracleCatalog['trigger_cols'])
        trigger_columns = {}
        print "get all trigger columns"
        for name, table_name, column_name, column_list, column_usage in self.__query(stmt):
            debug_message('debug: trigger %s column %s' % (name, column_name))
            t = trigger_columns.get(name)
            if not t:
                t = []
                trigger_columns[name] = t
            t.append((name, table_name, column_name, column_list, column_usage))
        return trigger_columns


    def __get_arguments(self):
        """Get all function/procedure argumets"""
#        stmt = """select object_name, package_name, argument_name, position, data_type, default_value, in_out, pls_type,
#            data_scale, data_precision, data_length
#                from user_arguments"""
        stmt = self._prepareStatement(OracleCatalog['arguments'])
        all_arguments = []
        print "get all pl/sql arguments"
        for name, package_name, argument_name, position, data_type, default_value, in_out, pls_type, data_scale, \
            data_precision, data_length in self.__query(stmt):
            debug_message('debug: pl/sql arguments - %s' % name)
            _data_type = ''
            if pls_type:
                _data_type = pls_type
            else:
                _data_type = data_type
            if data_type == 'NUMBER':
                if not data_precision:
                    data_precision = "38"
                _data_type = _data_type + '(%s' %data_precision
                if data_scale and data_scale <> 0:
                    _data_type = _data_type + ',%s' %data_scale
                _data_type = _data_type + ')'
            elif data_type in ('CHAR','VARCHAR2','NCHAR','NVARCHAR2','RAW','UROWID'):
                if data_length:
                    _data_type = _data_type + '(%s)' %data_length
            all_arguments.append\
                    ((name, package_name, argument_name, position, _data_type, default_value, in_out))
        return all_arguments


    def __get_user_source(self):
        """Get pl/sql source for procedures, functions and packages"""
#        stmt = "select name, type, line, text from user_source where type not like 'TYPE%' order by name, line"
        stmt = self._prepareStatement(OracleCatalog['source'])
        user_source = []
        print "get pl/sql source for procedures, functions and packages"
        for name, type, line, text in self.__query(stmt):
            debug_message('debug: pl/sql source - %s' % name)
            user_source.append((name, type, line, text))
        return user_source


    def __get_sequences (self):
        """Get user sequences"""
#        stmt = """select sequence_name, min_value, max_value, increment_by, cycle_flag, order_flag, cache_size
#                      from user_sequences"""
        stmt = self._prepareStatement(OracleCatalog['sequences'])
        sequences = {}
        print "get sequences"
        for name, min_value, max_value, step, cycled, ordered, cache_size in self.__query(stmt):
            sequences[name] = fpformat.fix(min_value,0), str(max_value), fpformat.fix(step,0), cycled, ordered, fpformat.fix(cache_size,0)
        return sequences


    def __get_types(self):
        """Get types"""
#        stmt = """select type_name, type_oid, typecode, attributes, methods,
#                      predefined, incomplete
#                    from user_types"""
        stmt = self._prepareStatement(OracleCatalog['types'])
        types = {}
        print "get types"
        for name, type_oid, typecode, attributes, methods, predefined, incomplete \
            in self.__query(stmt):
            debug_message('debug: type - %s' % name)
            types[name] = typecode, predefined, incomplete, type_oid, attributes, \
                 methods
        return types


    def __get_type_attributes(self):
        """Get type attributes from db"""
#        stmt = """select type_name, attr_name, attr_type_mod, attr_type_owner,
#                       attr_type_name, length, precision, scale, character_set_name,
#                       attr_no
#                    from user_type_attrs"""
        stmt = self._prepareStatement(OracleCatalog['type_attrs'])
        type_attributes = {}
        print "get type attributes from db"
        for type_name, attr_name, attr_type_mod, attr_type_owner, attr_type_name, \
            length, precision, scale, character_set_name, attr_no \
            in self.__query(stmt):
            debug_message('debug: type - %s attribute name %s' % (type_name, attr_name))
            t = type_attributes.get(type_name, None)
            if not t:
                t = {}

            t[attr_no] = attr_name, attr_type_mod, attr_type_owner, \
             attr_type_name, length, precision, scale, character_set_name
        return type_attributes


    def __get_type_methods(self):
        """get type methods from db"""
#        stmt = """select type_name, method_name, method_type, parameters, results
#                    from user_type_methods"""
        stmt = self._prepareStatement(OracleCatalog['type_methods'])
        type_methods = {}
        print "get type methods"
        for type_name, method_name, method_type, parameters, results \
            in self.__query(stmt):
            t = type_methods.get(type_name, None)
            if not t:
                t = {}
            t[method_name] = method_type, parameters, results
        return type_methods


    def _getJobs(self):
        """ Get old good jobs (dba_jobs). """
        print 'get database jobs'
        jobs = self.__query(self._prepareStatement(OracleCatalog['jobs']))
        return jobs


    def __getDependencies(self):
        """ Collect all dependencies in the { key : [deps], ... } format. """
        print 'get dependencies'
        deps = {}
        for name, referenced_owner, referenced_name, \
            referenced_link_name, referenced_type, dependency_type \
            in self.__query(self._prepareStatement(OracleCatalog['dependencies'])):
            if not deps.has_key(name):
                deps[name] = []
            deps[name].append([referenced_owner, referenced_name, referenced_link_name, referenced_type, dependency_type])
        return deps


    def __query(self, querystr):
        """Execute query end return results in array"""
        cur = self.cfg.connection.cursor()
        cur.execute(querystr)
        results = cur.fetchall()
        cur.close()
        return results


    def _prepareStatement(self, stmt):
        if self.cfg.useOwners == False:
            stmt = stmt.userSql()
        else:
            if len(self.cfg.owners) == 0:
                stmt = stmt.ownerSql()
            else:
                inClause = []
                for i in self.cfg.owners:
                    inClause.append("'%s'" % i.upper())
                stmt = stmt.ownerSql(inClause="%s, %s" % (self.cfg.currentUser, ','.join(inClause)))
        return stmt


if __name__ == '__main__':
    import cx_Oracle
    from osdconfig import OSDConfig
    c = OSDConfig()
    c.connection = cx_Oracle.connect('buap/p6a6u3b0@cpd_prod')
    s = OraSchemaDataDictionary(c)
    #print s.all_java_sources

