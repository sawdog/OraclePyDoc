"""Dia UML Diagram XML File Generator"""
import os


class DiaUmlDiagramGenerator:
    """ Creates dummy DIA file.
    It tries to gzip the file if possible
    TODO: clever placement of the objects in diagram."""

    def __init__(self, schema, filename, description, debug_mode, conf_file, compress=True):

        self.schema = schema
        self.filename = filename
        self.description = description

        # prepare file header
        header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        header += '<dia:diagram xmlns:dia="http://www.lysator.liu.se/~alla/dia/">\n'
        header += ' <dia:diagramdata>\n'
        header += '    <dia:attribute name="background">\n'
        header += '      <dia:color val="#ffffff"/>\n'
        header += '    </dia:attribute>\n'
        header += '    <dia:attribute name="paper">\n'
        header += '      <dia:composite type="paper">\n'
        header += '        <dia:attribute name="name">\n'
        header += '          <dia:string>#A4#</dia:string>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="tmargin">\n'
        header += '          <dia:real val="2.8222"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="bmargin">\n'
        header += '          <dia:real val="2.8222"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="lmargin">\n'
        header += '          <dia:real val="2.8222"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="rmargin">\n'
        header += '          <dia:real val="2.8222"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="is_portrait">\n'
        header += '          <dia:boolean val="true"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="scaling">\n'
        header += '          <dia:real val="1"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="fitto">\n'
        header += '          <dia:boolean val="false"/>\n'
        header += '        </dia:attribute>\n'
        header += '      </dia:composite>\n'
        header += '    </dia:attribute>\n'
        header += '   <dia:attribute name="grid">\n'
        header += '      <dia:composite type="grid">\n'
        header += '        <dia:attribute name="width_x">\n'
        header += '          <dia:real val="1"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="width_y">\n'
        header += '          <dia:real val="1"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="visible_x">\n'
        header += '          <dia:int val="1"/>\n'
        header += '        </dia:attribute>\n'
        header += '        <dia:attribute name="visible_y">\n'
        header += '          <dia:int val="1"/>\n'
        header += '        </dia:attribute>\n'
        header += '      </dia:composite>\n'
        header += '    </dia:attribute>\n'
        header += '    <dia:attribute name="guides">\n'
        header += '      <dia:composite type="guides">\n'
        header += '        <dia:attribute name="hguides"/>\n'
        header += '        <dia:attribute name="vguides"/>\n'
        header += '      </dia:composite>\n'
        header += '    </dia:attribute>\n'
        header += '  </dia:diagramdata>\n'
        header += '  <dia:layer name="Background" visible="true">\n'

        table_ids = {}
        i = 0
        table_text = ''
        self.export_tables = self.get_tables_for_export(conf_file)

        for table in self.schema.tables:
            if self.export_tables.count(table.name) == 0:
                continue
            i = i+1
            table_ids[table.name] = i
            table_text += '    <dia:object type="UML - Class" version="0" id="%s">\n' % i
            table_text += '      <dia:attribute name="name">\n'
            table_text += '        <dia:string>#%s#</dia:string>\n'  % table.name
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="abstract">\n'
            table_text += '        <dia:boolean val="false"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="suppress_attributes">\n'
            table_text += '        <dia:boolean val="false"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="suppress_operations">\n'
            table_text += '        <dia:boolean val="true"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="visible_attributes">\n'
            table_text += '        <dia:boolean val="true"/>\n'
            table_text += '      </dia:attribute>\n'

            table_text += '      <dia:attribute name="visible_operations">\n'
            table_text += '        <dia:boolean val="false"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="foreground_color">\n'
            table_text += '        <dia:color val="#000000"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="background_color">\n'
            table_text += '        <dia:color val="#ffffff"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="normal_font">\n'
            table_text += '        <dia:font name="Helvetica"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="abstract_font">\n'
            table_text += '        <dia:font name="NewCenturySchoolbook-Roman"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="classname_font">\n'
            table_text += '        <dia:font name="Helvetica-BoldOblique"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="abstract_classname_font">\n'
            table_text += '        <dia:font name="Times-Bold"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="font_height">\n'
            table_text += '        <dia:real val="0.6"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="abstract_font_height">\n'
            table_text += '        <dia:real val="0.6"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="classname_font_height">\n'
            table_text += '        <dia:real val="0.7"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="abstract_classname_font_height">\n'
            table_text += '        <dia:real val="1"/>\n'
            table_text += '      </dia:attribute>\n'

            table_text += self.get_columns_text(table)
            table_text += self.get_constraints_text(table)
            table_text += '      <dia:attribute name="visible_operations">\n'
            table_text += '        <dia:boolean val="false"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="operations"/>\n'
            table_text += '      <dia:attribute name="template">\n'
            table_text += '        <dia:boolean val="false"/>\n'
            table_text += '      </dia:attribute>\n'
            table_text += '      <dia:attribute name="templates"/>\n'
            table_text += '    </dia:object>\n'

        # link components together
        cs_text = ''
        table_id = 0
        constraint_count = 0
        for table in self.schema.tables:
            if table.referential_constraints:
                for cs in table.referential_constraints:
                    if self.export_tables.count(cs.table_name) == 0 or self.export_tables.count(cs.r_table) == 0:
                        continue
                    i = i + 1
                    col_list = reduce(lambda c1, c2: c1 + ', ' + c2, cs.columns.values())
                    t_id = table_ids[table.name]
                    col_pos = 7 + int(self.get_col_pos(cs.columns[1], table))
                    r_t_id = table_ids[cs.r_table]
                    r_cs = filter(lambda c, z=cs: c.name == z.r_constraint_name, self.schema.constraints)[0]
                    r_table = filter(lambda t, x=cs: t.name == x.r_table, self.schema.tables)[0]
                    r_col_pos = 7 + int(self.get_col_pos(r_cs.columns[1], r_table))
                    cs_text += '    <dia:object type="UML - Constraint" version="0" id="%s">\n' % i
                    cs_text += '      <dia:attribute name="constraint">\n'
                    cs_text += '        <dia:string>#%s#</dia:string>\n' % col_list
                    cs_text += '      </dia:attribute>\n'
                    cs_text += '      <dia:connections>\n'
                    cs_text += '        <dia:connection handle="0" to="%s" connection="%s"/>\n' % (t_id, col_pos)
                    cs_text += '        <dia:connection handle="1" to="%s" connection="%s"/>\n' % (r_t_id, r_col_pos)
                    cs_text += '      </dia:connections>\n'
                    cs_text += '    </dia:object>\n'

        footer = '  </dia:layer>\n'
        footer += '</dia:diagram>\n'


        print 'GZIPping...'
        try:
            if not compress:
                raise Exception
            import gzip
            f = gzip.GzipFile(self.filename, 'w')
            f.write(header + table_text + cs_text + footer)
            f.close()
        except IOError, e:
            print 'Cannot write to file "%s": %s' %(self.filename, e)
        except:
            if not compress:
                print 'GZIP passed. Running raw text writting'
            else:
                print 'GZIP failed. Running raw text writting'

            try:
                f = open(self.filename, 'w')
                f.write(header + table_text + cs_text + footer)
                f.close()
            except IOError, e:
                print 'Cannot write to plain file "%s": %s' % (self.filename, e)

        print 'Done\n'


    def get_columns_text(self, table):
        columns = table.columns
        if table.primary_key:
            pk_columns = table.primary_key.columns.values()
        else:
            pk_columns = None
        text = ''

        for i in range(len(columns)):
            column = columns[i+1]
            nullable_text = ''
            if column.nullable == 'N':
               nullable_text =  ' not null'
            text += '        <dia:composite type="umlattribute">\n'
            text += '          <dia:attribute name="name">\n'
            text += '            <dia:string>#%s#</dia:string>\n' % column.name
            text += '          </dia:attribute>\n'
            text += '          <dia:attribute name="type">\n'
            text += '            <dia:string>#%s#</dia:string>\n' % column.data_type + nullable_text
            text += '          </dia:attribute>\n'

            # handle default value
            if column.data_default:
                text += '          <dia:attribute name="value">\n'
                text += '            <dia:string>#%s#</dia:string>\n' % column.data_default
                text += '          </dia:attribute>\n'
            else:
                text += '          <dia:attribute name="value">\n'
                text += '            <dia:string/>\n'
                text += '          </dia:attribute>\n'

            v_type = '3'
            if pk_columns and pk_columns.count(column.name) > 0:
                v_type = '2'

            text += '          <dia:attribute name="visibility">\n'
            text += '            <dia:enum val="%s"/>\n' % v_type
            text += '          </dia:attribute>\n'
            text += '          <dia:attribute name="abstract">\n'
            text += '            <dia:boolean val="false"/>\n'
            text += '          </dia:attribute>\n'
            text += '            <dia:attribute name="class_scope">\n'
            text += '          <dia:boolean val="false"/>\n'
            text += '            </dia:attribute>\n'
            text += '        </dia:composite>\n'

        return '       <dia:attribute name="attributes">\n' + text + '</dia:attribute>\n'


    def get_constraints_text(self, table):
        if table.referential_constraints:

            cs_text = ''
            for cs in table.referential_constraints:
                if self.export_tables.count(cs.r_table) == 0:
                    continue
                name = cs.name

                cs_text += '      <dia:composite type="umloperation">\n'
                cs_text += '        <dia:attribute name="name">\n'
                cs_text += '          <dia:string>##</dia:string>\n'
                cs_text += '        </dia:attribute>\n'
                cs_text += '        <dia:attribute name="visibility">\n'
                cs_text += '          <dia:enum val="3"/>\n'
                cs_text += '        </dia:attribute>\n'
                cs_text += '        <dia:attribute name="abstract">\n'
                cs_text += '          <dia:boolean val="false"/>\n'
                cs_text += '        </dia:attribute>\n'
                cs_text += '        <dia:attribute name="class_scope">\n'
                cs_text += '          <dia:boolean val="false"/>\n'
                cs_text += '        </dia:attribute>\n'
                cs_text += '        <dia:attribute name="parameters">\n'
                cs_text += '          <dia:composite type="umlparameter">\n'
                cs_text += '            <dia:attribute name="name">\n'
                cs_text += '              <dia:string>#%s#</dia:string>\n' % name
                cs_text += '            </dia:attribute>\n'
                cs_text += '            <dia:attribute name="value">\n'
                cs_text += '              <dia:string/>\n'
                cs_text += '            </dia:attribute>\n'
                cs_text += '            <dia:attribute name="kind">\n'
                cs_text += '              <dia:enum val="0"/>\n'
                cs_text += '            </dia:attribute>\n'
                cs_text += '          </dia:composite>\n'
                cs_text += '        </dia:attribute>\n'
                cs_text += '      </dia:composite>\n'
            return cs_text
        else:
            return '''        <dia:attribute name="visible_operations">
          <dia:boolean val="false"/>
        </dia:attribute>
        <dia:attribute name="operations"/>\n'''


    def get_col_pos(self, column_name, table):
        i = 0
        for j in table.columns.keys():
            i = i + 1
            if table.columns[j].name == column_name:
                return i


    def get_tables_for_export(self, conf_file):
        r_list = []
        if conf_file:
            f = open(conf_file, 'r')
            t_list = f.readlines()
            for t in t_list:
                if t and t.strip() != '':
                    r_list.append(t.strip().upper())
        else:
            r_list = map(lambda t: t.name, self.schema.tables)
        return r_list


if __name__ == '__main__':
    import cx_Oracle
    import orasdict
    import oraschema
    connection = cx_Oracle.connect('s0/s0@test1')
    s = orasdict.OraSchemaDataDictionary(connection, 'Oracle',0)
    schema = oraschema.OracleSchema(s,0)
    doclet = DiaUmlDiagramGenerator(schema, ".", "vtr Data Model", "Really cool project",0,None, False)

