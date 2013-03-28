""" reST Doc Generator

    used with tools like sphinx

    XXX the writer portion should be generalized and we just need to
    have specific formatters....


    Todo:  Have all syntax highlighting handled by a single code formatter.
           Make the oracle objects python objects, then we can have shared logic:
             View and MView have nearly duplicate 'render/write' logic.

"""

# python imports
import os
import shutil
import string
from string import join
from string import lower
from string import strip

# package imports
from oraclepydoc.formatter.rest import reSTFormatter
from oraclepydoc.analyze import SchemaAnalyzer
from oraclepydoc.sqlhighlighter import SqlHighlighter
from oraclepydoc.dot import Dot
from oraclepydoc.oraverbose import set_verbose_mode
from oraclepydoc.oraverbose import debug_message


class reSTWriter(object):


    def __init__(self, cfg):

        set_verbose_mode(cfg.verbose_mode)
        self.dotEngine = Dot(cfg.output_dir)
        self.cfg = cfg
        self.formatter = reSTFormatter(cfg)
        self.index = {}
        self.syntaxHighlighter = SqlHighlighter(
                highlight=cfg.syntaxHighlighting)

        # write the reST files
        debug_message('\nCreating reST output')
        self._print_index_frames()
        self._print_list_pages()
        self._sanity_check()
        self._print_common_pages()

        debug_message('print tables')
        for table in cfg.schema.tables:
            self._print_table(table)

        debug_message('print views')
        for view in cfg.schema.views:
            self._print_view(view)

        debug_message('print materialized views')
        for mview in cfg.schema.mviews:
            self._print_mview(mview)

        debug_message('print functions')
        for function in cfg.schema.functions:
            self._print_function(function)

        debug_message('print procedures')
        for procedure in cfg.schema.procedures:
            self._print_procedure(procedure)

        debug_message('print sequences')
        for sequence in cfg.schema.sequences:
            self._print_sequence(sequence)

        debug_message('print packages')
        for package in cfg.schema.packages:
            self._print_package(package)

        debug_message('print java sources')
        for jsource in cfg.schema.java_sources:
            self._print_java_source(jsource)

        #self._print_symbol_index_page()


    def triggerAnchorType(self, trigger):
        """ Returns the string with object name trigger belongs to.
            E.g. 'view' for INSTEAD OF triggers, table for common trg etc.
            See docwidgets.py href_to_trigger() """
        if trigger.type == 'INSTEAD OF':
            return 'view'
        return 'table'

    def ddlSourceHref(self, name):
        cfg = self.cfg
        if not cfg.allowDDL or \
                not cfg.schema.ddlSource.scriptCache.has_key(name):
            return ''

        href = self.formatter.download_href(
                cfg.schema.ddlSource.scriptCache[name], 'DDL script')
        return href.replace('\\', '\\\\')


    def _print_index_frames(self):
        """print index frames.

           How we link to real pages are handled by toctree's

           links to anchors in the various pages are done by simply
           generating ':ref:' links.

        """
        cfg = self.cfg
        formatter = self.formatter
        schema = cfg.schema

        # tables
        rows = ['tables-list']
        for table in schema.tables:
            # XXX not sure how to offset this here....
            # because we are generating a toctree....
            #if table.secondary == 'Yes':
            #    link = self.formatter.i(link)
            rows.append(formatter.table_label(table.name))

        header = '%s Tables' % cfg.name
        self._print_toc_frame(header, rows, 'tables-index.rst')

        # indexes
        # not *real* pages.
        rows = [formatter.href(formatter.header_link('indexes-list')), '\n']
        for index in schema.indexes:
            rows.append(formatter.br())
            link = formatter.href_to_index(index.name, index.table_name,
                    index.name)
            rows.append(link)
            rows.append(formatter.br())
        self._print_index_frame('%s Indexes' % cfg.name, rows,
                'indexes-index.rst')

        # constraints
        rows = [formatter.href(formatter.header_link('constraints-list')),
                '\n']
        for con in schema.constraints:
            rows.append(formatter.br())
            link = formatter.href_to_constraint(con.name, con.table_name,
                    con.name)
            rows.append(link)
            rows.append(formatter.br())
        self._print_index_frame('%s Constraints' % cfg.name, rows,
                'constraints-index.rst')

        # views
        rows = ['views-list']
        for view in schema.views:
            rows.append(formatter.view_label(view.name))
        header = '%s Views' % cfg.name
        self._print_toc_frame(header, rows, 'views-index.rst')

        # materialized views
        rows = ['materialized_views-list']
        for mview in schema.mviews:
            rows.append(formatter.materialized_view_label(mview.name))
        header = '%s Materialized Views' % cfg.name
        self._print_toc_frame(header, rows, 'mviews-index.rst')

        #procedures
        rows = ['procedures-list']
        for procedure in schema.procedures:
            rows.append(formatter.procedure_label(procedure.name))
        header = '%s Procedures' % cfg.name
        self._print_toc_frame(header, rows, 'procedures-index.rst')

        #functions
        rows = ['functions-list']
        for function in schema.functions:
            rows.append(self.formatter.function_label(function.name))
        header = '%s Functions' % cfg.name
        self._print_toc_frame(header, rows, 'functions-index.rst')

        #packages
        rows = ['packages-list']
        for package in schema.packages:
            rows.append(formatter.package_label(package.name))
        header = '%s Packages' % cfg.name
        self._print_toc_frame(header, rows, 'packages-index.rst')

        #triggers
        rows = [formatter.href(formatter.header_link('triggers-list')), '\n']
        for trigger in schema.triggers:
            rows.append(formatter.br())
            link = self.formatter.href_to_trigger(trigger.name,
                    trigger.table_name, trigger.name,
                    self.triggerAnchorType(trigger))
            rows.append(link)
            rows.append(formatter.br())
        header = '%s Triggers' % cfg.name
        self._print_index_frame(header, rows, 'triggers-index.rst')

        #sequences
        rows = ['sequences-list']
        for sequence in schema.sequences:
            rows.append(self.formatter.sequence_label(sequence.name))
        header = '%s Sequences' % cfg.name
        self._print_toc_frame(header, rows, 'sequences-index.rst')

        #java sources
        rows = [formatter.href(formatter.header_link('java-sources-list')),
                '\n']
        for jsoursce in schema.java_sources:
            link = self.formatter.href_to_java_source(jsoursce.name)
            rows.append(link)
        header = '%s Java Sources' % cfg.name
        self._print_index_frame(header, rows, 'java-sources-index.rst')

    def _print_list_pages(self):
        """print list pages"""
        cfg = self.cfg
        formatter = self.formatter
        #tables
        rows = []
        for table in cfg.schema.tables:
            name = formatter.href_to_table(table.name)
            if table.secondary == 'Yes':
                # XXX ?
                name = formatter.i(name)

            comments = table.comments
            if comments:
                comments = formatter.pre(comments[:50]+'...')
            rows.append((name, comments, self.ddlSourceHref(table.name)))

        headers = ('Table', 'Description', 'DDL Script')
        file_name = 'tables-list'
        ht_table = formatter.table('Summary Tables List', headers, rows,
                heading_level=1)
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #indexes
        rows = []
        for index in cfg.schema.indexes:
            name = formatter.href_to_index(index.name, index.table_name,
                    index.name)
            #add entry to do index
            self._add_index_entry(index.name, name, 'index on table %s' %\
                    index.table_name)
            type = index.type
            table_name = formatter.href_to_table(index.table_name)
            rows.append((name, type, table_name,
                self.ddlSourceHref(index.name)))
        headers = ('Index', 'Type', 'Table', 'DDL Script')
        ht_table = formatter.table('Summary Indexes List', headers, rows,
                heading_level=1)
        file_name = 'indexes-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #triggers
        rows = []
        for trigger in cfg.schema.triggers:
            name = formatter.href_to_trigger(trigger.name, trigger.table_name,
                    trigger.name, self.triggerAnchorType(trigger))
            #add entry to do index
            self._add_index_entry(trigger.name, name,
                    'Trigger on %s %s' % (self.triggerAnchorType(trigger),
                        trigger.table_name))

            type = trigger.type
            if self.triggerAnchorType(trigger) == 'table':
                 table_name = formatter.href_to_table(trigger.table_name)
            else:
                 table_name = self.formatter.href_to_view(trigger.table_name)

            rows.append((name, type, table_name,
                self.ddlSourceHref(trigger.name)))
        headers = ('Trigger', 'Type', 'Table or View', 'DDL Script')
        ht_table = formatter.table('Summary Triggers List', headers, rows,
                heading_level=1)
        file_name = 'triggers-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #constraints
        rows = []
        for constraint in cfg.schema.constraints:
            name = formatter.href_to_constraint(constraint.name,
                    constraint.table_name, constraint.name)
            # add entry to doc index
            self._add_index_entry(constraint.name, name,
                    'constraint on table %s' % constraint.table_name)
            type = constraint.type
            table_name = formatter.href_to_table(constraint.table_name)
            rows.append((name, type, table_name,
                self.ddlSourceHref(constraint.name)))
        headers = ('Name', 'Type', 'Table', 'DDL Script')
        ht_table = formatter.table('Summary Constraints List', headers, rows,
                heading_level=1)
        file_name = 'constraints-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #views
        rows = []
        for view in cfg.schema.views:
            name = formatter.href_to_view(view.name)
            # add entry to doc index
            self._add_index_entry(view.name, name, 'view')
            comments = view.comments
            if comments:
                comments = formatter._quotehtml(comments[:50]+'...')
            rows.append((name, comments, self.ddlSourceHref(view.name)))
        headers = ('View', 'Description', 'DDL Script')
        ht_table = formatter.table('Summary Views List', headers, rows,
                heading_level=1)
        file_name = 'views-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        # mviews
        rows = []
        for mview in cfg.schema.mviews:
            name = formatter.href_to_materialized_view(mview.name)
            # add entry to doc index
            self._add_index_entry(mview.name, name, 'materialized view')
            rows.append([name, self.ddlSourceHref(mview.name)])
        headers = 'Materialized View', 'DDL Script'
        ht_table = formatter.table('Summary Materialized Views List', headers,
                rows, heading_level=1)
        file_name = 'materialized_views-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #procedures
        rows = []
        for procedure in cfg.schema.procedures:
            name = formatter.href_to_procedure(procedure.name)
            # add entry to doc index
            self._add_index_entry(procedure.name, name, 'procedure')
            rows.append([name, self.ddlSourceHref(procedure.name)])
        headers = ('Name', 'DDL Script')
        ht_table = formatter.table('Summary Procedures List', headers, rows,
                heading_level=1)
        file_name = 'procedures-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #functions
        rows = []
        for function in cfg.schema.functions:
            name = formatter.href_to_function(function.name)
            # add entry to doc index
            self._add_index_entry(function.name, name, 'function')
            row = ([name, self.ddlSourceHref(function.name)])
            rows.append(row)
        headers = ('Name', 'DDL Script')
        ht_table = formatter.table('Summary Functions List', headers, rows,
                heading_level=1)
        file_name = 'functions-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #packages
        rows = []
        for package in cfg.schema.packages:
            name = formatter.href_to_package(package.name)
            # add entry to doc index
            self._add_index_entry(package.name, name, 'package')
            row = ([name, self.ddlSourceHref(package.name)])
            rows.append(row)

        headers = ('Name', 'DDL Script')
        ht_table = formatter.table('Summary Packages List', headers, rows,
                heading_level=1)
        file_name = 'packages-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #sequences
        rows = []
        for s in cfg.schema.sequences:
            rows.append((s.getName() + formatter.anchor(s.getName()),
                         s.getMinValue(), s.getMaxValue(), s.getStep(),
                         s.isCycled(), s.isOrdered(), s.getCacheSize(),
                         self.ddlSourceHref(s.getName())))
            self._add_index_entry(s.getName(),
                    formatter.href_to_sequence(s.getName()), 'index')
        headers = ('Name', 'Min Value', 'Max Value', 'Step', 'Cycled',
                'Ordered', 'Cache Size', 'DDL Script')
        ht_table = formatter.table('Summary Sequences List', headers, rows,
                heading_level=1)
        file_name = 'sequences-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        #java sources
        rows = []
        for jsource in cfg.schema.java_sources:
            name = formatter.href_to_java_source(jsource.name)
            self._add_index_entry(jsource.name, name, 'java source')
            row = ([name])
            rows.append(row)
        if not rows:
            rows.append(('None', ' '))
        headers = ('Name', ' ')
        ht_table = formatter.table('Summary Java Sources List', headers, rows,
                heading_level=1)
        file_name = 'java-sources-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

        # jobs
        rows = []
        for i in cfg.schema.jobs:
            self.syntaxHighlighter.setStatement(i.what)
            self.syntaxHighlighter.parse()
            rows.append((i.job, i.log_user, i.priv_user,
                         i.schema_user, i.total_time, i.broken,
                         i.interval, i.failures, self.syntaxHighlighter.getOutput()))
            self._add_index_entry('JOB-%s' % i.job,
                    formatter.href_to_job('JOB-%s' % i.job), 'database job')
        headers = (['Job', 'log_user', 'priv_user', 'schema_user', 'total_time', 'broken',
                    'interval', 'failures', 'what'])
        ht_table = formatter.table('Summary Jobs List', headers, rows,
                heading_level=1)
        file_name = 'jobs-list'
        self._print_list_page(formatter.page_header(file_name) + ht_table,
                file_name)

    def _htmlizeTrigger(self, trigger):
        """A common XHTML trigger writter for all tables
            and views (materialized or normal) """
        formatter = self.formatter
        text = []
        text.append(formatter.anchor('trg-%s' % trigger.name))
        text.append(formatter.heading(trigger.name, 3))
        description = join(trigger.description.split('\n'), '\n   ')
        trigg = """.. code-block:: sql\n\n   CREATE TRIGGER %s%s\n   """ %\
                (description, trigger.referencing_names)

        if trigger.when_clause:
            trigg += "   When \n   %s\n" % formatter._quotehtml(trigger.when_clause)

        # go through the trigger body and indent for our code block
        body = trigger.body.split('\n')
        trigg += formatter._quotehtml(join(body, '\n   '))
        text.append(trigg)
        return join(text, '')


    def _print_table(self, table):
        """print table page"""
        text = []
        cfg = self.cfg
        formatter = self.formatter
        # lable used in generating anchors back to the 'section' in the table
        label = formatter.table_label(table.name)
        text.append(formatter.page_header(label))
        text.append(formatter.heading(table.name, 1))

        # punt entry in doc index
        # XXX what is the index entry?
        self._add_index_entry(table.name, formatter.href_to_table(table.name), 'table')

        # print comments
        if table.comments:
            text.append(formatter.p(formatter._quotehtml(table.comments)))

        # link to the table DDL file.
        text.append(self.ddlSourceHref(table.name))
        text.extend([formatter.br(), formatter.br()])

        rows = []
        # fixme iot table overflow segment column problem
        if len(table.columns) > 0:
            for i in range(len(table.columns)):
                column = table.columns[i + 1]
                self._add_index_entry(column.name,
                        formatter.href_to_column(column.name, table.name,
                            column.name), 'column of table %s' % table.name)

                # XXX Anchors in tables???   Grrrr. create the anchor
                #rows.append(formatter.anchor('col-%s' % column.name))
                rows.append((column.name, column.data_type, column.nullable,
                        column.data_default, column.comments))

            headers = ('Name', 'Type', 'Nullable', 'Default', 'Comment')
            text.append(formatter.table('Columns', headers, rows,
                heading_level=2))

        # create the constraints listing, the various constraint types are
        # sub categories of the overall constraint category.
        # print primary key

        # in the constraints-index.rst page there is a link for ea. constraint
        # back to the 'constraints section' for ea. obj which has constraints.
        # For now, this is generalised to simply the top of the section
        # due to not being sure how to create anchors in table rows.
        #
        # The anchor needs to be unique.
        anchor = '%s-constraints' % label
        text.append(formatter.anchor(anchor))
        text.append(formatter.heading('Constraints', 2))

        if table.primary_key:
            # XXX Can anchors go above items that are not headers?
            #pk_name = formatter.anchor('cs-%s' % table.primary_key.name) +\
            #        table.primary_key.name
            pk_columns = ''

            for i in range(len(table.primary_key.columns)):
                pk_columns = pk_columns + formatter.href_to_column(
                        table.primary_key.columns[i + 1],
                        table.name, table.primary_key.columns[i + 1])

                if i + 1 != len(table.primary_key.columns):
                    pk_columns = pk_columns + ', '

            headers = ('Constraint', 'Columns')
            rows = [(table.primary_key.name, pk_columns)]
            anchor = '%s-primary_key' % label
            text.append(formatter.table('Primary Key', headers, rows, anchor=anchor,
                heading_level=3))

        # print check constraints
        if table.check_constraints:
            rows = []
            for constraint in table.check_constraints:
                # XXX anchors to rows....
                #rows.append((constraint.name + formatter.anchor('cs-%s' %\
                #        constraint.name), formatter._quotehtml(constraint.check_cond)))
                rows.append((constraint.name,
                    formatter._quotehtml(constraint.check_cond)))

            headers = ('Constraint', 'Check Condition')
            anchor = '%s-check_constraints' % label
            text.append(formatter.table('Check Constraints', headers, rows,
                anchor=anchor, heading_level=3))

        #print referential constraints
        if table.referential_constraints:
            rows = [] # html table
            aList = [] # list for dot image
            for constraint in table.referential_constraints:
                aList.append(constraint.r_table)
                columns = ''
                for i in range(len(constraint.columns)):
                    columns = columns + formatter.href_to_column(
                            constraint.columns[i + 1], table.name,
                            constraint.columns[i + 1])
                    if i + 1 != len(constraint.columns):
                        columns = columns + ', '

                # XXX anchor in table rows....
                #name = constraint.name + formatter.anchor("cs-%s" % constraint.name)
                name = constraint.name
                r_table = formatter.href_to_table(constraint.r_table)
                r_constraint_name = formatter.href_to_constraint(
                        constraint.r_constraint_name, constraint.r_table,
                        constraint.r_constraint_name)
                rows.append((name, columns, r_table, r_constraint_name,
                    constraint.delete_rule))

            headers = ('Constraint', 'Columns', 'Referencing',
                    'Constraint', 'Delete')
            anchor = '%s-foreign_keys' % label
            text.append(formatter.table('Foreign Keys', headers, rows,
                anchor=anchor, heading_level=3))

            if self.dotEngine.haveDot:
                text.append(formatter.heading('ERD Diagram', 4))
                # append more references - the 2nd side of FKs
                inverseList = []
                if table.referenced_by != None:
                    for table_name, constraint_name in table.referenced_by:
                        inverseList.append(table_name)

                imgname = self.dotEngine.fileGraphList(table.name, aList,
                        inverseList, reST=True)
                if imgname != None:
                    map_name = '%s' % table.name + '.map'
                    try:
                        f = file(os.path.join(cfg.output_dir, map_name), 'r')
                        text.append(formatter.imgMap(table.name, f.read()))
                        f.close()
                        os.remove(os.path.join(cfg.output_dir, map_name))
                    except IOError:
                        print 'error reading %s' % map_name

                    text.append(formatter.p(formatter.img_raw(imgname,
                        htmlMap=table.name)))

        # print unique keys
        if table.unique_keys:
            rows = []
            for constraint in table.unique_keys:
                columns = ''
                for i in range(len(constraint.columns)):
                    columns = columns + formatter.href_to_column(
                            constraint.columns[i + 1], table.name,
                            constraint.columns[i + 1])
                    if i+1 != len(constraint.columns):
                        columns = columns + ', '
                # XXX anchor in table rows
                #name = constraint.name + formatter.anchor("cs-%s" % constraint.name)
                name = constraint.name
                rows.append((name, columns))

            headers = ('Constraint', 'Columns')
            anchor = '%s-unique_keys' % label
            text.append(formatter.table('Unique Keys', headers, rows,
                anchor=anchor, heading_level=3))

        # print table options
        rows = []
        rows.append(('Tablespace', table.tablespace_name))
        rows.append(('Index Organized', table.index_organized))
        rows.append(('Generated by Oracle', table.secondary))
        rows.append(('Clustered', table.clustered))

        if table.clustered == 'Yes':
            rows.append(('Cluster', table.cluster_name))

        rows.append(('Nested', table.nested))
        rows.append(('Temporary', table.temporary))
        headers = ('Option', 'Settings')
        text.append(formatter.table('Options', headers, rows, heading_level=2))

        # print indexes
        if table.indexes:
           rows = []
           for index in table.indexes:
               columns = ''
               for i in  range(len(index.columns)):
                    columns = columns + formatter.href_to_column(
                            index.columns[i + 1], table.name,
                            index.columns[i + 1])
                    if i + 1 != len(index.columns):
                        columns = columns + ', '
               # XXX anchors in rows....
               #rows.append(formatter.anchor('ind-%s' % index.name))
               #rows.append(formatter.br())
               rows.append((index.name, index.type, index.uniqueness, columns,
                   self.ddlSourceHref(index.name)))

           headers = ('Index Name', 'Type', 'Unuqueness', 'Columns',
                   'DDL script')
           # in the indexes-index.rst page there is a link for ea. index
           # back to the 'indexes table' for ea. obj which has indexes.
           # For now, this is generalised to simply the top of the table
           # due to not being sure how to create anchors in table rows.
           #
           # The anchor needs to be unique.
           anchor = '%s-index-table' % label
           text.append(formatter.table('Indexes', headers, rows, anchor=anchor,
               heading_level=2))

        # print list of tables with references to this table
        if table.referenced_by:
            rows = []
            for table_name, constraint_name in table.referenced_by:
                constraint_name = formatter.href_to_constraint(constraint_name,
                        table_name, constraint_name)

                table_name = formatter.href_to_table(table_name)
                rows.append((table_name, constraint_name))

            headers = ('Table', 'Constraint')
            text.append(formatter.table('Referenced By', headers, rows,
                heading_level=2))

        # print triggers
        if table.triggers:
            text.append(formatter.anchor('%s-triggers' % label))
            text.append(formatter.heading('Triggers', 2))

            for trigger in table.triggers:
                text.append(self._htmlizeTrigger(trigger))

        # print partitions
        if table.tab_partitions:
            #text.append(formatter.heading('Partitions', 2))
            rows = []
            for partition in table.tab_partitions:
                rows.append([partition.partition_name, str(partition.partition_position),
                            partition.tablespace_name, str(partition.high_value)])

            headers = ('Partition', 'Position', 'Tablespace', 'High Value')
            text.append(formatter.table('Partitions', headers, rows,
                heading_level=2))

        # dependencies
        text.append(self._printDependencies(table.name))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir,
                '%s.rst' % label)
        self._write(''.join(text), file_name)

    def _print_view(self, view):
        """print view page"""
        text = []
        cfg = self.cfg
        formatter = self.formatter
        label = formatter.view_label(view.name)
        text.append(formatter.page_header(label))
        text.append(formatter.heading(view.name, 1))

        # print comments
        if view.comments:
            text.append(formatter.p(formatter._quotehtml(view.comments)))

        # link to the view ddl file
        text.append(self.ddlSourceHref(view.name))
        text.extend([formatter.br(), formatter.br()])

        rows = []
        for i in range(len(view.columns)):
            column = view.columns[i + 1]
            # add entry to doc index
            self._add_index_entry(column.name,
                    formatter.href_to_view_column(column.name, view.name,
                        column.name), 'column of of view %s' % view.name)

            # XXX Anchors in tables?
            #rows.append(formatter.anchor('col-%s' % column.name))
            rows.append((column.name, column.data_type, column.nullable,
                column.insertable, column.updatable, column.deletable,
                column.comments))

        headers = ('Name', 'Type', 'Nullable','Insertable', 'Updatable',
                'Deletable', 'Comment')
        text.append(formatter.table('Columns', headers, rows, heading_level=2))

        # print query
        text.append(formatter.heading('Query', 2))
        code_text = join(view.text.split('\n'), '\n   ')
        text.append(""".. code-block:: sql\n\n   %s""" % code_text)
        #self.syntaxHighlighter.setStatement(view.text)
        #self.syntaxHighlighter.parse()
        #text.append(formatter.pre(self.syntaxHighlighter.getHeader()))
        #text.append(formatter.pre(self.syntaxHighlighter.getOutput()))

        # print constraints
        if view.constraints:
            rows = []
            for constraint in view.constraints:
                # XXX grrrr anchors in rows....
                #rows.append((constraint.name + \
                #        formatter.anchor('cs-%s' % constraint.name),constraint.type))
                rows.append((constraint.name, constraint.type))

            headers = ('Constraint', 'Type')
            anchor = '%s-constraints' % label
            text.append(formatter.table('Constraints', headers, rows,
                anchor=anchor, heading_level=2))

        # print triggers
        if view.triggers:
            text.append(formatter.anchor('%s-triggers' % label))
            text.append(formatter.heading('Triggers',3))
            for trigger in view.triggers:
                text.append(self._htmlizeTrigger(trigger))

        text.extend([formatter.br(), formatter.br()])
        # dependencies
        text.append(self._printDependencies(view.name))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir, '%s.rst' % label)
        self._write(''.join(text), file_name)

    def _print_mview(self, mview):
        """print materialized view - treated as a table also"""
        text = []
        cfg = self.cfg
        formatter = self.formatter
        label = formatter.materialized_view_label(mview.name)
        text.append(formatter.page_header(label))
        text.append(formatter.heading(mview.name, 1))

        container = formatter.href_to_materialized_view(mview.container)
        rows = [(container, mview.mv_updatable)]
        headers = ('Container', 'Updatable')
        text.append(formatter.table(None, headers, rows))

        # print comments
        if mview.comments:
            text.append(formatter.p(formatter._quotehtml(mview.comments)))

        # link to the view ddl file
        text.append(self.ddlSourceHref(mview.name))
        text.extend([formatter.br(), formatter.br()])

        rows = []
        for i in range(len(mview.columns)):
            column = mview.columns[i + 1]

            # XXX what's this for?
            # add entry to doc index
            self._add_index_entry(column.name,
                    formatter.href_to_view_column(column.name, mview.name,
                        column.name), 'column of of view %s' % mview.name)

            # XXX anchors in table rows, grrr
            #rows.append((column.name + formatter.anchor('col-%s' % column.name),
            #    column.data_type, column.nullable, column.insertable,
            #    column.updatable, column.deletable, column.comments))
            rows.append((column.name, column.data_type, column.nullable,
                column.insertable, column.updatable, column.deletable,
                column.comments))

        headers = ('Name', 'Type', 'Nullable', 'Insertable', 'Updatable',
                'Deletable', 'Comment')
        text.append(formatter.table('Columns', headers, rows))

        # print query
        text.append(formatter.heading('Query', 2))
        code_text = join(mview.query.split('\n'), '\n   ')
        text.append(""".. code-block:: sql\n\n   %s""" % code_text)
        #self.syntaxHighlighter.setStatement(mview.query)
        #self.syntaxHighlighter.parse()
        #text.append(formatter.pre(self.syntaxHighlighter.getHeader()))
        #text.append(formatter.pre(self.syntaxHighlighter.getOutput()))

        # print constraints
        if mview.constraints:
            title = 'Constraints'
            rows = []
            for constraint in mview.constraints:
                # Anchors in rows again
                #rows.append((constraint.name + formatter.anchor('cs-%s' %\
                #        constraint.name), constraint.type))
                rows.append((constraint.name, constraint.type))
            headers = ('Constraint Name', 'Type')
            anchor = '%s-constraints' % label
            text.append(formatter.table('Constraints', headers, rows,
                anchor=anchor, heading_level=2))

        # print triggers
        if mview.triggers:
            text.append(formatter.anchor('%s-triggers' % label))
            text.append(formatter.heading('Triggers',3))
            for trigger in mview.triggers:
                text.append(self._htmlizeTrigger(trigger))

        text.extend([formatter.br(), formatter.br()])
        # dependencies
        text.append(self._printDependencies(mview.name))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir, '%s.rst' % label)
        self._write(''.join(text), file_name)

    def _print_procedure(self, procedure):
        """print procedure page"""
        text = []
        cfg = self.cfg
        formatter = self.formatter
        label = formatter.procedure_label(procedure.name)
        text.append(formatter.page_header(label))
        text.append(formatter.heading(procedure.name, 1))

        # print the procedure arguments
        rows = []
        for argument in procedure.arguments:
            if argument.default_value:
                _default_value = argument.default_value
            else:
                _default_value = ''

            row = (argument.name, argument.data_type,
                formatter._quotehtml(_default_value), argument.in_out)
            rows.append(row)

        headers = ('Name', 'Data Type', 'Default Value', 'In/Out')
        text.append(formatter.table('Arguments', headers, rows,
            heading_level=2))

        # link to the view ddl file
        text.append(self.ddlSourceHref(procedure.name))
        text.extend([formatter.br(), formatter.br()])

        # print procedure source
        anchor = '%s-source' % label
        text.append(formatter.anchor(anchor))
        text.append(formatter.heading('Source', 2))
        _src = []

        # XXX - if there is only 1 line - how to behave?
        # It is possible, and we could add \n on specific keywords?

        for line in procedure.source.source:
            # XXX might be able to use ''.format here....
            # the args in the procedure are padded with 56 ' ' --
            # so remove some of it....
            if line.text.find(55 * ' ') == 0:
                line.text = line.text.replace(' ', '', 35)

            _src.append('%s: %s' % (string.rjust(str(line.line_no), 3),
                line.text))

        code_text = join(_src, '\n   ')
        text.append(""".. code-block:: sql\n\n   %s""" % code_text)
        #self.syntaxHighlighter.setStatement(''.join(_src))
        #self.syntaxHighlighter.parse()
        #text.append(formatter.pre(self.syntaxHighlighter.getHeader()))
        #text.append(formatter.pre(self.syntaxHighlighter.getOutput()))

        # dependencies
        text.extend([formatter.br(), formatter.br()])
        text.append(self._printDependencies(procedure.name))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir, '%s.rst' % label)
        self._write(''.join(text), file_name)

    def _print_sequence(self, sequence):
        """print sequence page"""
        # create header and context bar
        text = []
        cfg = self.cfg
        formatter = self.formatter
        label = formatter.sequence_label(sequence.name)
        text.append(formatter.page_header('%s' % label))
        text.append(formatter.heading(sequence.name, 1))

        # print the sequence
        rows = [(sequence.name, sequence.min, sequence.max, sequence.increment,
                sequence.cache, sequence.cycled, sequence.ordered)]
        headers = ('Name', 'Min', 'Max', 'Increment By', 'Cache',
                'Cycled', 'Ordered')
        text.append(formatter.table(None, headers, rows))

        # link to the view ddl file
        text.append(self.ddlSourceHref(sequence.name))
        text.extend([formatter.br(), formatter.br()])

        # XXX does oracle track the sequence dependencies/referenced by?
        #text.append(self._printDependencies(procedure.name))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir, '%s.rst' % label)
        self._write(''.join(text), file_name)

    def _print_function(self, function):
        """print function page"""
        text = []
        cfg = self.cfg
        formatter = self.formatter
        label = formatter.function_label(function.name)
        text.append(formatter.page_header('%s' % label))
        text.append(formatter.heading(function.name, 1))
        # overview or summary info....
        text.append('Function - %s returns %s' % (function.name,
            function.return_data_type))
        text.extend([formatter.br(), formatter.br()])
        text.append(self.ddlSourceHref(function.name))
        text.extend([formatter.br(), formatter.br()])

        # create the args table
        headers = ('Name', 'Data Type', 'Default', 'In/Out')
        rows = []
        for argument in function.arguments:
            if argument.default_value:
                _default_value = argument.default_value
            else:
                _default_value = ''
            rows.append([argument.name, argument.data_type,
                    formatter._quotehtml(_default_value), argument.in_out])
        text.append(formatter.table('Arguments', headers, rows, heading_level=3))
        text.append(formatter.heading('Returns', 3))
        text.append(function.return_data_type)

        text.append(formatter.heading('Source', 2))
        _src = []
        for line in function.source.source:
            # XXX might be able to use ''.format here....
            # the args in the procedure are padded with 45 ' ' --
            # so remove some of it....
            if line.text.find(44 * ' ') == 0:
                line.text = line.text.replace(' ', '', 15)

            _src.append('%s: %s' % (string.rjust(str(line.line_no), 3),
                line.text))

        code_text = join(_src, '\n   ')
        text.append(""".. code-block:: sql\n\n   %s""" % code_text)
        #self.syntaxHighlighter.setStatement(''.join(_src))
        #self.syntaxHighlighter.parse()
        #text.append(formatter.pre(self.syntaxHighlighter.getHeader()))
        #text.append(formatter.pre(self.syntaxHighlighter.getOutput()))

        # dependencies
        text.extend([formatter.br(), formatter.br()])
        text.append(self._printDependencies(function.name))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir, '%s.rst' % label)
        self._write(''.join(text), file_name)

    def _print_package(self, package):
        """print package page"""
        text = []
        cfg = self.cfg
        formatter = self.formatter
        label = formatter.package_label(package.name)
        text.append(formatter.page_header('%s' % label))
        text.append(formatter.heading(package.name, 1))
        text.append(self.ddlSourceHref(package.name))
        text.extend([formatter.br(), formatter.br()])
        _src = []
        for line in package.source.source:
            _src.append(string.rjust(str(line.line_no),6) + ': ' +  line.text)

        #self.syntaxHighlighter.setStatement(''.join(_src))
        #self.syntaxHighlighter.parse()
        text.append(formatter.heading('Package Source', 2))
        #text.append(formatter.pre(self.syntaxHighlighter.getHeader()))
        #text.append(formatter.pre(self.syntaxHighlighter.getOutput()))

        if package.body_source:
            _src = []
            text.append(formatter.heading('Body', 3))
            for line in package.body_source.source:
                # XXX might be able to use ''.format here....
                # the args in the package are padded with 45 ' ' --
                # so remove some of it....
                if line.text.find(44 * ' ') == 0:
                    line.text = line.text.replace(' ', '', 15)

                _src.append('%s: %s' % (string.rjust(str(line.line_no), 3),
                    line.text))

            code_text = join(_src, '\n   ')
            text.append(""".. code-block:: sql\n\n   %s""" % code_text)
            #self.syntaxHighlighter.setStatement(''.join(_src))
            #self.syntaxHighlighter.parse()
            #text.append(formatter.pre(self.syntaxHighlighter.getHeader()))
            #text.append(formatter.pre(self.syntaxHighlighter.getOutput()))

        # dependencies
        text.append(formatter.br())
        text.append(self._printDependencies(package.name))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir,
                '%s.rst' % label)
        self._write(''.join(text), file_name)

    def _print_java_source(self, java_source):
        """print function page"""
        text = []
        cfg = self.cfg
        formatter = self.formatter
        label = formatter.java_source_label(java_source.name)
        text.append(formatter.page_header('%s' % label))
        text.append(formatter.heading('Java source %s' % java_source.name, 1))

        _src = []
        for line in java_source.source:
            _src.append(string.rjust(str(line.line_no),6) + ': ')
            # in java source empty string is None, so need to check before adding text
            if line.text:
                _src.append(line.text)
            _src.append('\n')
        text.append(formatter.pre(formatter._quotehtml(''.join(_src))))

        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir, '%s.rst' % label)
        self._write(''.join(text), file_name)


    def _print_symbol_index_page(self):
        cfg = self.cfg
        formatter = self.formatter
        debug_message('print symbols index page')
        text = []
        text.append(formatter.page_header('Schema Objects Index'))
        local_nav_bar = []

        keys = self.index.keys()
        keys.sort()
        letter = ''
        for key in keys:
            if (key[:1] != letter):
                letter = key[:1]
                local_nav_bar.append((letter,letter))
        text.append(formatter.context_bar(local_nav_bar))

        letter = ''
        for key in keys:
            if (key[:1] != letter):
                letter = key[:1]
                text.append(formatter.heading(letter, 3) +\
                        formatter.anchor(letter))
            for entry in self.index[key]:
                text.append('%s %s<br/>' % entry)
        text.append(formatter.page_footer())
        file_name = os.path.join(cfg.output_dir, 'symbol-index.rst')
        self._write(''.join(text), file_name)


    def _sanity_check(self):
        cfg = self.cfg
        br = self.formatter.br
        debug_message('print sanity check page')
        problems = False
        text = []
        text.append(self.formatter.heading('Sanity Check', 1))
        text.append(br())

        scheck = SchemaAnalyzer(cfg.connection, cfg.schema)
        if scheck.fk_no_indexes:
            text.append(self.formatter.anchor('fk-ix'))
            text.append(br())
            text.append(self.formatter.heading(
                'No indexes on columns involved in foreign key constraints', 2))
            text.append(br())
            text.append('  You should almost always index foreign keys. The '\
                    'only exception is when the matching unique or primary '\
                    'key is never updated or deleted. For more information '\
                    'take a look at `Concurrency Control, Indexes, and Foreign Keys <http://docs.oracle.com/cd/B13789_01/server.101/b10743/data_int.htm>`_')
            text.append(br())
            text.append(br())
            text.append('  The sql file which will generate these indexes '\
                    'is :download:`created for you <./sql_sources/fk-indexes.sql>`')
            text.append(br())
            text.append(br())
            title = '"Unindexed" foreign keys'
            headers = 'Table Name', 'Constraint name', 'Columns'
            rows = []
            for constraint in scheck.fk_no_indexes:
                row=[]
                row.append(self.formatter.href_to_table(constraint.table_name))
                row.append(self.formatter.href_to_constraint(constraint.name,
                    constraint.table_name, constraint.name))
                columns = ''
                columns_count = len(constraint.columns)
                i=0
                for j in constraint.columns.keys():
                    columns += constraint.columns[j]
                    i +=1
                    if i != columns_count:
                        columns += ', '
                row.append(columns)
                rows.append(row)
                #write sql
            # XXX the sql files go into a single directory
            # when sphinx parses the output...so we need to have more complex
            # names for our files to avoid clashing.
            file_name = os.path.join(cfg.output_dir,
                    '%s-fk-indexes.sql' % cfg.fpname)
            self._write(scheck.fk_no_indexes_sql, file_name)
            text.append(self.formatter.table(title, headers, rows))
            problems = True

        if len(scheck.invalids) != 0:
            problems = True
            text.append(self.formatter.anchor('inv'))
            text.append(br())
            text.append(self.formatter.heading('Invalid objects', 2))
            text.append(br())
            text.append('  Invalid object does not mean a problem sometimes. '\
                    'Sometimes it will fix itself as is is executed or '\
                    'accessed.  But if there is an error in USER_ERRORS '\
                    'table, you are in trouble then...')
            text.append(br())
            text.append(br())
            text.append('  The sql file which will compile these objects '\
                    'is :download:`created for you <./compile-objects.sql>`')
            text.append(br())
            self._write(scheck.invalids_sql, os.path.join(cfg.output_dir, 'compile-objects.sql'))
            invalids = scheck.invalids
            for i in invalids:
                if i[1] == 'PACKAGE' or i[1] == 'PACKAGE BODY':
                    i[0] = self.formatter.href_to_package(i[0])
                if i[1] == 'PROCEDURE':
                    i[0] = self.formatter.href_to_procedure(i[0])
                if i[1] == 'FUNCTION':
                    i[0] = self.formatter.href_to_function(i[0])
                if i[1] == 'VIEW':
                    i[0] = self.formatter.href_to_view(i[0])
                if i[1] == 'TRIGGER':
                    for j in cfg.schema.triggers:
                        if j.name == i[0]:
                            i[0] = self.formatter.href_to_trigger(i[0],
                                    j.table_name, i[0],
                                    self.triggerAnchorType(j))
                            break
                # XXX  ?
                #i[2] = self.formatter._quotehtml(i[2])
            text.append(self.formatter.table('Invalids',
                ['Object name', 'Type', 'Error', 'At line'], invalids))

        if problems == False:
            # no checks
            text.append(self.formatter.p('All is well on the western front.'))

        file_name = os.path.join(cfg.output_dir, 'sanity-check.rst')
        self._write(''.join(text), file_name)


    def _write(self, text, file_name):
        # write file to fs
        debug_message('debug: writing file %s' % file_name)
        f = open(file_name, 'w')
        f.write(text)
        f.close()


    def _add_index_entry(self, key , link, description):
        # add new entry to symbol index
        t = self.index.get(key)
        if not t:
            self.index[key] = t = []
        t.append((link, description))


    def _gen_nav_id(self, name=None):
        """generate a nav page name..."""
        return name and '%s-nav' or 'nav'

    def _print_common_pages(self):
        """write out the high level toc pages.

           XXX this is not factored into the formatter as it should be...
        """
        cfg = self.cfg
        formatter = self.formatter
        name = cfg.name
        nav_id = self._gen_nav_id()
        text = []
        text.append('.. _%s:\n' % name.replace(' ', '-'))
        text.append('.. _%s:\n' % nav_id)
        text.append('.. index::\n')
        text.append('    %s' % name)
        text.extend([formatter.br(), formatter.br()])
        text.append(formatter.heading('%s DB Documentation' % name, 1))
        text.append(formatter.br())
        # add some table info above the toc
        text.append(formatter._main_frame(cfg.name,
                cfg.desc, self.syntaxHighlighter.highlight))
        text.append(formatter.br())
        text.append(formatter._global_toc())

        # create the main db erd from the schema
        imgname = None
        if self.dotEngine.haveDot:
            erdDict = {}
            for table in cfg.schema.tables:
                refs = []
                if table.referential_constraints:
                    for ref in table.referential_constraints:
                        refs.append(ref.r_table)
                erdDict[table.name] = refs
                map_name = lower(name.replace(' ', '_'))

            imgname = self.dotEngine.fileGraphDict(erdDict, reST=True,
                    name=map_name)
            if imgname != None:
                try:
                    f = file(os.path.join(cfg.output_dir, '%s.map' % map_name),
                            'r')
                    itext = formatter.imgMap('mainmap', f.read())
                    f.close()
                    os.remove(os.path.join(cfg.output_dir, '%s.map' % map_name))
                except IOError:
                    itext = ''
                    debug_message('error reading %s.map GraphViz file' % \
                            map_name)

                imgname = itext + formatter.img_raw(imgname,
                        htmlMap='mainmap', cssClass='erd')
            else:
                imagename = 'No ERD Generated.'

        #XXX main erd image needs to follow the global_toc
        text.extend([formatter.br(), formatter.br()])
        text.append(formatter.heading('ERD Diagram', 2))
        text.append(formatter.br())
        text.append(imgname)
        file_name = os.path.join(cfg.output_dir, nav_id + '.rst')
        self._write(join(text, ''), file_name)

    def _print_index_frame(self, header, item_list, file_name):
        """Index frames are for items which do not have *real* .rst files to
           point to.....

         generic procedure to print index page::

                  header    - title string, i.e "Tables"
                  item_list - :ref: formatted links to items.
                  file_name - relative file name to write out

        """
        f_name = os.path.join(self.cfg.output_dir, file_name.replace('/', '-'))
        self._write(self.formatter._index_frame(header, item_list, file_name),
                f_name)

    def _print_toc_frame(self, header, item_list, file_name):
        """Index frame really is a toctree for the 'type' being listed.

         generic procedure to print index page::

                  header    - title string, i.e "Tables"
                  item_list - list of rst page names
                  file_name - relative file name to write out

        """
        text = self.formatter._toc_frame(header, item_list, file_name)
        f_name = os.path.join(self.cfg.output_dir, file_name.replace('/', '-'))
        self._write(text, f_name)


    def _print_list_page(self, text, file_name):
        """write the page out to disk"""
        file_name = strip(file_name) + '.rst'
        debug_message('writing %s page' % file_name)
        file_name = os.path.join(self.cfg.output_dir,
                file_name.replace('/', '-'))
        self._write(text, file_name)


    def _haveDependencies(self, key):
        return self.cfg.schema.dependencies.has_key(key)

    def _printDependencies(self, key):
        """ Prints the dependecy table for given key/object """
        if (self._haveDependencies(key)):
            rows = []
            schema = self.cfg.schema
            schema_name = schema.name
            # go through all the rows and construct links to all the
            # dependencies....
            # XXX by convention, we are assuming that schemas not of this
            # run will be created with `-o schema_name` so that we can
            # programmatically link to other schemas here.
            for dep in self.cfg.schema.dependencies[key]:
                rowner, rname, rlink, rtype, dtype = dep

                # first thing to check is if there are no Referenced Types
                # then we can pass on the meth func lookup.
                if rtype == 'NON-EXISTENT':
                    # do nothing....no link will be created.
                    pass
                else:
                    # generate meth call for the appropriate type.
                    if rowner == schema_name:
                        meth = 'href_to_%s' % lower(rtype.replace(' ', '_'))
                        rname = getattr(self.formatter, meth)(rname)
                    else:
                        meth = '%s_label' % lower(rtype)
                        meth = meth.replace(' ', '_')
                        # we could potentially raise here if the meth
                        # does not exist - that's ok, we need to know this
                        # and handle it.
                        link = '../%s/%s' % (lower(rowner),
                                getattr(self.formatter, meth)(rname))
                        rname = self.formatter.doc(link, rname)

                rows.append([rowner, rname, rlink, rtype, dtype])

            headers = ('Ref Owner', 'Referenced Name',
                    'Referenced Link', 'Ref Type', 'Dependency')
            return self.formatter.table('Dependencies', headers, rows,
                    anchor='deps')
        else:
            return ''


if __name__ == '__main__':
    import cx_Oracle
    import orasdict
    import oraschema
    from osdconfig import OSDConfig
    c = OSDConfig()
    c.connection = cx_Oracle.connect('s0/asgaard')
    c.dictionary = orasdict.OraSchemaDataDictionary(c)
    c.schema = oraschema.OracleSchema(c)
    doclet = OraSchemaDoclet(c)

