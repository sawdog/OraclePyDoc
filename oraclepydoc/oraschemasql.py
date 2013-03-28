""" Oracle catalog queries """


class OracleCatalogStatement:

    def __init__(self, userSql='', ownerSql='', ownerColumn='owner'):
        self._userSql = userSql
        self._ownerSql = ownerSql
        self._ownerColumn = ownerColumn

    def userSql(self):
        return self._userSql

    def ownerSql(self, inClause=None):
        if inClause == None:
            return self._ownerSql % 'where 1=1'
        return self._ownerSql % ('where %s in (%s)' % (self._ownerColumn, inClause))


OracleCatalog = {

    'tables' : OracleCatalogStatement(
                userSql="""select table_name, partitioned, secondary, cluster_name,
                            iot_type, temporary,  nested, tablespace_name
                            from user_tables""",
                ownerSql="""select owner||'.'||table_name, partitioned, secondary, cluster_name,
                            iot_type, temporary,  nested, tablespace_name
                            from all_tables %s"""
               ),

    'tab_partitions': OracleCatalogStatement(
                userSql='''select table_name, partition_name,
                            tablespace_name, high_value,
                            partition_position
                            from user_tab_partitions order by table_name, partition_position''',
                ownerSql='''select table_owner||'.'||table_name, partition_name,
                            tablespace_name, high_value,
                            partition_position
                            from all_tab_partitions %s order by table_owner||'.'||table_name, partition_position''',
                ownerColumn='table_owner'
                ),

    'tab_comments' : OracleCatalogStatement(
                userSql="""SELECT table_name, comments
                            FROM user_tab_comments
                            WHERE comments is not null""",
                ownerSql="""SELECT owner||'.'||table_name, comments
                            FROM all_tab_comments
                            %s
                            and comments is not null"""
                ),

    'col_comments' : OracleCatalogStatement(
                userSql="""SELECT table_name, column_name, comments
                            FROM user_col_comments
                            where comments is not null""",
                ownerSql="""SELECT owner||'.'||table_name, column_name, comments
                            FROM all_col_comments
                            %s
                            and comments is not null"""
                ),

    'columns' : OracleCatalogStatement(
                userSql="""select table_name, column_name, data_type , data_length, data_precision,
                             data_scale, nullable, column_id, data_default
                            from user_tab_columns
                            order by table_name, column_id""",
                ownerSql="""select owner||'.'||table_name, column_name, data_type , data_length, data_precision,
                             data_scale, nullable, column_id, data_default
                            from all_tab_columns
                            %s
                            order by owner||'.'||table_name, column_id"""
                ),

    'constraints' : OracleCatalogStatement(
                userSql="""select table_name, constraint_name, constraint_type, search_condition, r_owner,
                            r_constraint_name , delete_rule
                            from user_constraints where r_owner is null or r_owner = user""",
                ownerSql="""select owner||'.'||table_name, owner||'.'||constraint_name, constraint_type, search_condition, r_owner,
                            r_owner||'.'||r_constraint_name , delete_rule
                            from all_constraints
                            %s
                            --and r_owner is null --or r_owner = user"""
                ),

    'cons_columns' : OracleCatalogStatement(
                userSql="""select constraint_name, table_name, column_name, position from
                            user_cons_columns""",
                ownerSql="""select owner||'.'||constraint_name, owner||'.'||table_name, column_name, position
                            from all_cons_columns
                            %s"""
                ),

    'views' : OracleCatalogStatement(
                userSql="""select view_name, text from user_views""",
                ownerSql="""select owner||'.'||view_name, text from all_views %s"""
                ),

    'mviews' : OracleCatalogStatement(
                userSql="""select mview_name, container_name, query, updatable from user_mviews""",
                ownerSql="""select owner||'.'||mview_name, container_name, query, updatable from all_mviews %s"""
                ),

    'indexes' : OracleCatalogStatement(
                userSql="""select index_name, table_name, index_type, uniqueness, include_column, generated, secondary
                            from user_indexes""",
                ownerSql="""select owner||'.'||index_name, owner||'.'||table_name, index_type, uniqueness, include_column, generated, secondary
                            from all_indexes %s"""
                ),

    'ind_columns' : OracleCatalogStatement(
                userSql="""select index_name, table_name, column_name, column_position from user_ind_columns""",
                ownerSql="""select index_owner||'.'||index_name, table_owner||'.'||table_name, column_name, column_position
                            from all_ind_columns %s""",
                ownerColumn='index_owner'
                ),

    'ind_expressions' : OracleCatalogStatement(
                userSql="""select index_name, table_name, column_expression, column_position from user_ind_expressions""",
                ownerSql="""select index_owner||'.'||index_name, table_owner||'.'||table_name, column_expression, column_position
                            from all_ind_expressions %s""",
                ownerColumn='index_owner'
                ),

    'updatable_columns' : OracleCatalogStatement(
                userSql="""select table_name, column_name, insertable, updatable, deletable
                            from all_updatable_columns
                            where table_name in (select view_name from user_views)""",
                ownerSql="""select owner||'.'||table_name, column_name, insertable, updatable, deletable
                            from all_updatable_columns %s"""
                ),

    'triggers' : OracleCatalogStatement(
                userSql="""select trigger_name, trigger_type, triggering_event, base_object_type, table_name,
                            column_name, referencing_names, when_clause, status, description, action_type, trigger_body
                            from user_triggers""",
                ownerSql="""select owner||'.'||trigger_name, trigger_type, triggering_event, base_object_type, table_owner||'.'||table_name,
                            column_name, referencing_names, when_clause, status, description, action_type, trigger_body
                            from all_triggers
                            %s"""
                ),

    'trigger_cols' : OracleCatalogStatement(
                userSql="select trigger_name, table_name, column_name, column_list, column_usage from user_trigger_cols",
                ownerSql="""select trigger_owner||'.'||trigger_name, table_owner||'.'||table_name, column_name, column_list, column_usage
                            from all_trigger_cols
                            %s""",
                ownerColumn='trigger_owner'
                ),

    'arguments' : OracleCatalogStatement(
                userSql="""select object_name, package_name, argument_name, position, data_type, default_value, in_out, pls_type,
                            data_scale, data_precision, data_length
                            from user_arguments""",
                ownerSql="""select owner||'.'||object_name, package_name, argument_name, position, data_type, default_value, in_out, pls_type,
                            data_scale, data_precision, data_length
                             from all_arguments
                             %s"""
                ),

    'source' : OracleCatalogStatement(
                userSql="select name, type, line, text from user_source where type not like 'TYPE%' order by name, line",
                ownerSql="""select owner||'.'||name, type, line, text
                            from all_source
                            %s
                            and type not like 'TYPE%%' order by name, line"""
                ),

    'sequences' : OracleCatalogStatement(
                userSql="""select sequence_name, min_value, max_value, increment_by, cycle_flag, order_flag, cache_size
                              from user_sequences""",
                ownerSql="""select sequence_owner||'.'||sequence_name, min_value, max_value, increment_by, cycle_flag, order_flag, cache_size
                            from all_sequences
                            %s""",
                ownerColumn='sequence_owner'
                ),

    'types' : OracleCatalogStatement(
                userSql="""select type_name, type_oid, typecode, attributes, methods,
                              predefined, incomplete
                            from user_types""",
                ownerSql="""select owner||'.'||type_name, type_oid, typecode, attributes, methods,
                              predefined, incomplete
                            from all_types
                            %s"""
                ),

    'type_attrs' : OracleCatalogStatement(
                userSql="""select type_name, attr_name, attr_type_mod, attr_type_owner,
                           attr_type_name, length, precision, scale, character_set_name,
                           attr_no
                            from user_type_attrs""",
                ownerSql="""select owner||'.'||type_name, attr_name, attr_type_mod, attr_type_owner,
                               attr_type_name, length, precision, scale, character_set_name,
                               attr_no
                             from all_type_attrs
                             %s"""
                ),

    'type_methods' : OracleCatalogStatement(
                userSql="""select type_name, method_name, method_type, parameters, results
                            from user_type_methods""",
                ownerSql="""select owner||'.'||type_name, method_name, method_type, parameters, results
                               from all_type_methods %s"""
                ),

    'jobs' : OracleCatalogStatement(
                userSql="""select job, log_user, priv_user, schema_user, total_time, broken,
                              interval, failures, what
                              from user_jobs""",
                ownerSql="""select job, log_user, priv_user, schema_user, total_time, broken,
                              interval, failures, what
                              from all_jobs %s""",
                ownerColumn='priv_user'
                ),

    'dependencies' : OracleCatalogStatement(
                userSql = """select name, referenced_owner, referenced_name, referenced_link_name,
                                    referenced_type, dependency_type
                                from user_dependencies""",
                ownerSql = """select owner||'.'||name, referenced_owner, referenced_name, referenced_link_name,
                                     referenced_type, dependency_type
                                from all_dependencies
                                %s"""
                )

}



if __name__ == '__main__':
    print OracleCatalog['tables'].userSql()
    print OracleCatalog['tables'].ownerSql()
    print OracleCatalog['tab_partitions'].userSql()
    print OracleCatalog['tab_partitions'].ownerSql("'BUAP','FOO'")
    print OracleCatalog['tab_comments'].ownerSql("'BUAP','FOO'")
    print OracleCatalog['dependencies'].userSql()
    print OracleCatalog['dependencies'].ownerSql("'FOO', 'BAR'")

