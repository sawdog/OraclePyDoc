class SchemaAnalyzer:

    def __init__(self, connection, schema):
        self.schema = schema
        self.connection = connection
        self.name_prefix = 'fk_no_index_'
        self.fk_no_indexes = []
        self.fk_no_indexes_sql = ''
        self.invalids = []
        self.invalids_sql = ''

        self._analyze_fk_indexes()
        self._checkInvalidObjects()


    def _analyze_fk_indexes(self):
        j = 0
        for table in self.schema.tables:
            if table.referential_constraints:
                for constraint in table.referential_constraints:
                    if self._find_index(constraint.columns, table.indexes) == 0:
                        self.fk_no_indexes.append(constraint)
                        self.fk_no_indexes_sql += "--missed index on %s table for %s constraint \n" \
                                                  % (table.name, constraint.name)
                        _columns = ''
                        for i in range(len(constraint.columns)):
                            _columns = _columns + constraint.columns[i+1] + ', '
                        self.fk_no_indexes_sql += "create index %s%s on %s (%s);\n\n" \
                                                  % (self.name_prefix, j , table.name , _columns[:-2])
                        j = j + 1


    def _find_index(self, columns, indexes):
        if not indexes:
            return 0
        else:
            for index in indexes:
                if len(columns) <= len(index.columns):
                    for i in range(len(columns)):
                        if columns[i+1] != index.columns[i+1]:
                            break
                        elif i+1 == len(columns):
                            return 1
            return 0


    def _checkInvalidObjects(self):
        stmt = '''select o.object_name, o.object_type, e.line, e.text
                    from user_objects o, user_errors e
                    where o.object_name = e.name (+)
                       and o.object_type = e.type (+)
                       and o.status != \'VALID\''''
        cur = self.connection.cursor()
        cur.execute(stmt)
        results = cur.fetchall()
        cur.close()
        used = []
        for name, type, line, msg in results:
            if msg == None:
                msg = 'No error. It will be fixed itself later.'
            else:
                if not used.count(name):
                    used.append(name)
                    if type == 'PACKAGE BODY':
                        mtype = 'PACKAGE'
                        mcompile = ' BODY;'
                    else:
                        mtype = type
                        mcompile = ';'
                    self.invalids_sql += 'ALTER %s %s COMPILE%s\n\n' % (mtype, name, mcompile)
            self.invalids.append([name, type, msg, line])


if __name__ == '__main__':
    import cx_Oracle
    import orasdict
    import oraschema
    connection = cx_Oracle.connect('aram_v1/aram_v1')
    s = orasdict.OraSchemaDataDictionary(connection, 'Oracle')
    schema = oraschema.OracleSchema(s)
    d = SchemaAnalyzer(schema)
    d._analyze_fk_indexes()
