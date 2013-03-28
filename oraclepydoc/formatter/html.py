""" HTML Generator """

from os import path
from os import remove
from shutil import copy
from string import rjust

from oraclepydoc.dot import Dot
from oraclepydoc.docwidgets import HtmlWidgets
from oraclepydoc.analyze import SchemaAnalyzer
from oraclepydoc.sqlhighlighter import SqlHighlighter
from oraclepydoc.oraverbose import set_verbose_mode
from oraclepydoc.oraverbose import debug_message


class HTMLFormatter(object):

    def __init__(self, cfg):
        set_verbose_mode(cfg.verbose_mode)
        self.syntaxHighlighter = SqlHighlighter(
                highlight=cfg.syntaxHighlighting)
        self.dotEngine = Dot(cfg.output_dir)
        self.cfg = cfg
        self.html = HtmlWidgets(cfg.name, cfg.css, cfg.webEncoding,
                cfg.notNulls)
        self.index = {}

        # print html files
        debug_message('\nCreating HTML output')
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

        debug_message('print packages')
        for package in cfg.schema.packages:
            self._print_package(package)

        debug_message('print java sources')
        for jsource in cfg.schema.java_sources:
            self._print_java_source(jsource)

        self._print_symbol_index_page()


    def _copy_css(self):
        """copy the css file to the output_dir"""
        debug_message('copying CSS stylesheet to output_dir')
        css = self.cfg.css
        output_dir = self.cfg.output_dir
        csspath = self.cfg.csspath
        try:
            copy(path.join(csspath, css), output_dir)
            debug_message('css: done')

        except IOError, (errno, errmsg):
            msg = path.join(csspath, css) + ' not fround. ' \
                        'Trying to find another.  Error copying CSS style. ' \
                        'You are running precompiled version propably.\n' \
                        'Related info: (%s) %s' % (errno, errmsg)
            debug_message(msg)
            try:
                debug_message('Trying: ' + path.join(path.dirname(
                        sys.executable), 'css', css))
                copy(path.join(path.dirname(sys.executable),
                    'css', css), output_dir)
                debug_message('css: done')
            except IOError:
                print 'Error: (%s) %s' % (errno, errmsg)
                print 'Please copy some css style into output directory manually.'

    def triggerAnchorType(self, trigger):
        """ Returns the string with object name trigger belongs to.
            E.g. 'view' for INSTEAD OF triggers, table for common trg etc.
            See docwidgets.py href_to_trigger() """
        if trigger.type == 'INSTEAD OF':
            return 'view'
        return 'table'


    def ddlSourceHref(self, name):
        if not self.cfg.allowDDL:
            return ''
        if not self.cfg.schema.ddlSource.scriptCache.has_key(name):
            return ''
        return self.html.href(self.cfg.schema.ddlSource.scriptCache[name], 'DDL script')


    def _print_index_frames(self):
        #
        # print index frames
        #

        # tables
        rows = []
        for table in self.cfg.schema.tables:
            link = self.html.href_to_table(table.name, "Main")
            if table.secondary == 'Yes':
                link = self.html.i(link)
            rows.append(link)
        self._print_index_frame("Tables", rows, "tables-index.html")

        # indexes
        rows = []
        for index in self.cfg.schema.indexes:
            link = self.html.href_to_index(index.name, index.table_name, index.name, "Main")
            rows.append(link)
        self._print_index_frame("Indexes", rows, "indexes-index.html")

        # constraints
        rows = []
        for constraint in self.cfg.schema.constraints:
            link = self.html.href_to_constraint(constraint.name, constraint.table_name, constraint.name, "Main")
            rows.append(link)
        self._print_index_frame("Constraints", rows, "constraints-index.html")

        # views
        rows = []
        for view in self.cfg.schema.views:
            link = self.html.href_to_view(view.name, "Main")
            rows.append(link)
        self._print_index_frame("Views", rows, "views-index.html")

        # materialized views
        rows = []
        for mview in self.cfg.schema.mviews:
            link = self.html.href_to_mview(mview.name, "Main")
            rows.append(link)
        self._print_index_frame("Materialized&nbsp;Views", rows, "mviews-index.html")

        #procedures
        rows = []
        for procedure in self.cfg.schema.procedures:
            link = self.html.href_to_procedure(procedure.name, "Main")
            rows.append(link)
        self._print_index_frame("Procedures", rows, "procedures-index.html")

        #functions
        rows = []
        for function in self.cfg.schema.functions:
            link = self.html.href_to_function(function.name, "Main")
            rows.append(link)
        self._print_index_frame("Functions", rows, "functions-index.html")

        #packages
        rows = []
        for package in self.cfg.schema.packages:
            link = self.html.href_to_package(package.name, "Main")
            rows.append(link)
        self._print_index_frame("Packages", rows, "packages-index.html")

        #triggers
        rows = []
        for trigger in self.cfg.schema.triggers:
            link = self.html.href_to_trigger(trigger.name, trigger.table_name,
                                             trigger.name, self.triggerAnchorType(trigger),
                                             "Main")
            rows.append(link)
        self._print_index_frame("Triggers", rows, "triggers-index.html")

        #sequences
        rows = []
        for sequence in self.cfg.schema.sequences:
            link = self.html.href_to_sequence(sequence.getName(), "Main")
            rows.append(link)
        self._print_index_frame("Sequences", rows, "sequences-index.html")

        #java sources
        rows = []
        for jsoursce in self.cfg.schema.java_sources:
            link = self.html.href_to_java_source(jsoursce.name, "Main")
            rows.append(link)
        self._print_index_frame("Java Sources", rows, "java-sources-index.html")


    def _print_list_pages(self):
        #
        # print list pages
        #

        #tables
        rows = []
        for table in self.cfg.schema.tables:
            name = self.html.href_to_table(table.name)
            if table.secondary == 'Yes':
                name = self.html.i(name)
            comments = table.comments
            if comments:
                comments = self.html._quotehtml(comments[:50]+'...')
            rows.append(( name, comments, self.ddlSourceHref(table.name) ))
        headers = "Table", "Description", 'DDL Script'
        ht_table = self.html.table("Tables", headers, rows)
        self._print_list_page("Tables", ht_table, "tables-list.html")

        #indexes
        rows = []
        for index in self.cfg.schema.indexes:
            name = self.html.href_to_index(index.name, index.table_name, index.name)
            #add entry to do index
            self._add_index_entry(index.name, name, "index on table %s" % index.table_name)
            type = index.type
            table_name = self.html.href_to_table(index.table_name)
            rows.append(( name, type, table_name, self.ddlSourceHref(index.name) ))
        headers = "Index", "Type", "Table", 'DDL Script'
        ht_table = self.html.table("Indexes", headers, rows)
        self._print_list_page("Indexes", ht_table, "indexes-list.html")

        #triggers
        rows = []
        for trigger in self.cfg.schema.triggers:
            name = self.html.href_to_trigger(trigger.name, trigger.table_name,
                                             trigger.name, self.triggerAnchorType(trigger))
            #add entry to do index
            self._add_index_entry(trigger.name, name,
                                  "Trigger on %s %s" % (self.triggerAnchorType(trigger), trigger.table_name))
            type = trigger.type
            if self.triggerAnchorType(trigger) == 'table':
                 table_name = self.html.href_to_table(trigger.table_name)
            else:
                 table_name = self.html.href_to_view(trigger.table_name)
            rows.append(( name, type, table_name, self.ddlSourceHref(trigger.name) ))
        headers = "Trigger", "Type", "Table or View", 'DDL Script'
        ht_table = self.html.table("Triggers", headers, rows)
        self._print_list_page("Triggers", ht_table, "triggers-list.html")

        #constraints
        rows = []
        for constraint in self.cfg.schema.constraints:
            name = self.html.href_to_constraint(constraint.name, constraint.table_name, constraint.name)
            # add entry to doc index
            self._add_index_entry(constraint.name, name, "constraint on table %s" % constraint.table_name)
            type = constraint.type
            table_name = self.html.href_to_table(constraint.table_name)
            rows.append(( name, type, table_name, self.ddlSourceHref(constraint.name) ))
        headers = "Name", "Type", "Table", 'DDL Script'
        ht_table = self.html.table("Constraints", headers, rows)
        self._print_list_page("Constraints", ht_table, "constraints-list.html")

        #views
        rows = []
        for view in self.cfg.schema.views:
            name = self.html.href_to_view(view.name)
            # add entry to doc index
            self._add_index_entry(view.name, name, "view")
            comments = view.comments
            if comments:
                comments = self.html._quotehtml(comments[:50]+'...')
            rows.append(( name, comments, self.ddlSourceHref(view.name) ))
        headers = "View", "Description", 'DDL Script'
        ht_table = self.html.table("Views", headers, rows)
        self._print_list_page("Views", ht_table, "views-list.html")

        # mviews
        rows = []
        for mview in self.cfg.schema.mviews:
            name = self.html.href_to_mview(mview.name)
            # add entry to doc index
            self._add_index_entry(mview.name, name, "materialized view")
            rows.append([name, self.ddlSourceHref(mview.name)])
        headers = "Materialized View", 'DDL Script'
        ht_table = self.html.table("Materialized Views", headers, rows)
        self._print_list_page("Materialized Views", ht_table, "mviews-list.html")

        #procedures
        rows = []
        for procedure in self.cfg.schema.procedures:
            name = self.html.href_to_procedure(procedure.name)
            # add entry to doc index
            self._add_index_entry(procedure.name, name, "procedure")
            rows.append([name, self.ddlSourceHref(procedure.name)])
        headers = "Name", 'DDL Script'
        ht_table = self.html.table("Procedures", headers, rows)
        self._print_list_page("Procedures", ht_table, "procedures-list.html")

        #functions
        rows = []
        for function in self.cfg.schema.functions:
            name = self.html.href_to_function(function.name)
            # add entry to doc index
            self._add_index_entry(function.name, name, "function")
            row = ([name, self.ddlSourceHref(function.name)])
            rows.append(row)
        headers = "Name", 'DDL Script'
        ht_table = self.html.table("Functions", headers, rows)
        self._print_list_page("Functions", ht_table, "functions-list.html")

        #packages
        rows = []
        for package in self.cfg.schema.packages:
            name = self.html.href_to_package(package.name)
            # add entry to doc index
            self._add_index_entry(package.name, name, "package")
            row = ([name, self.ddlSourceHref(package.name)])
            rows.append(row)
        headers = "Name", 'DDL Script'
        ht_table = self.html.table("Packages", headers, rows)
        self._print_list_page("Packages", ht_table, "packages-list.html")

        #sequences
        rows = []
        for s in self.cfg.schema.sequences:
            rows.append((s.getName() + self.html.anchor(s.getName()),
                         s.getMinValue(), s.getMaxValue(), s.getStep(),
                         s.isCycled(), s.isOrdered(), s.getCacheSize(),
                         self.ddlSourceHref(s.getName())))
            self._add_index_entry(s.getName(),
                                  self.html.href_to_sequence(s.getName()), "index")
        headers = "Name", "Min Value", "Max Value", "Step", "Cycled", "Ordered", \
                "Cache Size", 'DDL Script'
        ht_table = self.html.table("Sequences", headers, rows)
        self._print_list_page("Sequences", ht_table, "sequences.html")

        #java sources
        rows = []
        for jsource in self.cfg.schema.java_sources:
            name = self.html.href_to_java_source(jsource.name)
            self._add_index_entry(jsource.name, name, "java source")
            row = ([name])
            rows.append(row)
        headers = (["Name"])
        ht_table = self.html.table("Java Sources", headers, rows)
        self._print_list_page("Java Sources", ht_table, "java-sources-list.html")

        # jobs
        rows = []
        for i in self.cfg.schema.jobs:
            self.syntaxHighlighter.setStatement(i.what)
            self.syntaxHighlighter.parse()
            rows.append((i.job, i.log_user, i.priv_user,
                         i.schema_user, i.total_time, i.broken,
                         i.interval, i.failures, self.syntaxHighlighter.getOutput()))
            self._add_index_entry('JOB-%s' % i.job, self.html.href_to_job('JOB-%s' % i.job), 'database job')
        headers = (['Job', 'log_user', 'priv_user', 'schema_user', 'total_time', 'broken',
                    'interval', 'failures', 'what'])
        ht_table = self.html.table('Jobs', headers, rows)
        self._print_list_page('Jobs', ht_table, 'jobs.html')


    def _htmlizeTrigger(self, trigger):
        """ A common XHTML trigger writter for all tables
            and views (materialized or normal) """
        text = []
        text.append(self.html.anchor('trg-%s' % trigger.name))
        text.append(self.html.heading(trigger.name, 4))
        trigg = 'CREATE TRIGGER \n%s\n%s\n' % (trigger.description, trigger.referencing_names)
        if trigger.when_clause:
            trigg += "When \n%s\n" % self.html._quotehtml(trigger.when_clause)
        trigg += self.html._quotehtml(trigger.body)
        self.syntaxHighlighter.setStatement(trigg)
        self.syntaxHighlighter.parse()
        text.append(self.html.pre(self.syntaxHighlighter.getHeader()))
        text.append(self.html.pre(self.syntaxHighlighter.getOutput()))
        return ''.join(text)


    def _print_table(self, table):
        "print table page"
        # create header and context bar
        text = []
        text.append(self.html.page_header("Table-%s" % table.name))
        local_nav_bar = []
        local_nav_bar.append(("Description", "t-descr"))
        local_nav_bar.append(("Columns", "t-cols"))
        local_nav_bar.append(("Primary key", "t-pk"))
        local_nav_bar.append(("Check Constraints", "t-cc"))
        local_nav_bar.append(("Foreign keys", "t-fk"))
        local_nav_bar.append(("Unique Keys", "t-uc"))
        local_nav_bar.append(("Options", "t-opt"))
        local_nav_bar.append(("Indexes", "t-ind"))
        local_nav_bar.append(("Referenced by", "t-refs"))
        local_nav_bar.append(("Triggers", "t-trgs"))
        local_nav_bar.append(("Partitions", "t-parts"))
        if (self._haveDependencies(table.name)):
            local_nav_bar.append(("Dependencies", "deps"))

        text.append(self.html.context_bar(local_nav_bar))
        text.append(self.html.heading(table.name, 2))
        # punt entry in doc index
        self._add_index_entry(table.name, self.html.href_to_table(table.name), "table")
        # print comments
        if table.comments:
            text.append('%s %s' % (self.html.heading("Description:",3), self.html.anchor("t-descr")))
            text.append(self.html.p(self.html._quotehtml(table.comments)))
        text.append(self.ddlSourceHref(table.name))
        #print columns
        rows = []
        # fixme iot table overflow segment column problem
        if len(table.columns) > 0:
            for i in range(len(table.columns)):
                column = table.columns[i+1]
                self._add_index_entry(column.name, self.html.href_to_column(column.name, table.name, column.name),\
                                      "column of table %s" % table.name)
                rows.append((column.name+self.html.anchor('col-%s' % column.name), column.data_type, \
                             column.nullable, column.data_default, column.comments))
            headers = "Name", "Type", "Nullable", "Default value", "Comment"
            text.append(self.html.table("Columns" + self.html.anchor('t-cols'), headers, rows))
        # print primary key
        if table.primary_key:
            title = "Primary key:" + self.html.anchor("t-pk")
            pk_name = table.primary_key.name + self.html.anchor("cs-%s" % table.primary_key.name)
            pk_columns = ''
            for i in range(len(table.primary_key.columns)):
                pk_columns = pk_columns + \
                      self.html.href_to_column(table.primary_key.columns[i+1],table.name, table.primary_key.columns[i+1])
                if i+1 != len(table.primary_key.columns):
                    pk_columns = pk_columns + ', '
            headers = "Constraint Name" , "Columns"
            rows = []
            rows.append((pk_name, pk_columns))
            text.append(self.html.table( title, headers, rows))
        # print check constraints
        if table.check_constraints:
            title = "Check Constraints:" + self.html.anchor("t-cc")
            rows = []
            for constraint in table.check_constraints:
                rows.append((constraint.name + self.html.anchor("cs-%s" % constraint.name), \
                             self.html._quotehtml(constraint.check_cond)))
            text.append(self.html.table(title, ("Constraint Name","Check Condition"), rows))
        #print referential constraints
        if table.referential_constraints:
            title = "Foreign Keys:" + self.html.anchor("t-fk")
            # create an image
            rows = [] # html table
            aList = [] # list for dot image
            for constraint in table.referential_constraints:
                aList.append(constraint.r_table)
                columns = ''
                for i in range(len(constraint.columns)):
                    columns = columns + self.html.href_to_column(constraint.columns[i+1], \
                                                        table.name, constraint.columns[i+1])
                    if i+1 != len(constraint.columns):
                        columns = columns + ', '
                name = constraint.name + self.html.anchor("cs-%s" % constraint.name)
                r_table = self.html.href_to_table(constraint.r_table)
                r_constraint_name = self.html.href_to_constraint(constraint.r_constraint_name, \
                                                  constraint.r_table, constraint.r_constraint_name)
                rows.append((name, columns, r_table, r_constraint_name, constraint.delete_rule))
            headers = "Constraint Name", "Columns", "Referenced table", "Referenced Constraint", "On Delete Rule"
            text.append(self.html.table(title,headers, rows))
            if self.dotEngine.haveDot:
                # append more references - the 2nd side of FKs
                inverseList = []
                if table.referenced_by != None:
                    for table_name, constraint_name in table.referenced_by:
                        inverseList.append(table_name)

                imgname = self.dotEngine.fileGraphList(table.name, aList, inverseList)
                if imgname != None:
                    try:
                        f = file(path.join(self.cfg.output_dir, table.name+'.map'), 'r')
                        text.append(self.html.imgMap('erdmap', f.read()))
                        f.close()
                    except IOError:
                        print 'error reading %s' % table.name+'.map'
                    text.append(self.html.img(imgname, htmlMap='erdmap', cssClass='erd'))
        # print unique keys
        if table.unique_keys:
            title = "Unique Keys:" + self.html.anchor("t-uc")
            rows = []
            for constraint in table.unique_keys:
                columns = ''
                for i in range(len(constraint.columns)):
                    columns = columns + self.html.href_to_column(constraint.columns[i+1],table.name, \
                                                                 constraint.columns[i+1])
                    if i+1 != len(constraint.columns):
                        columns = columns + ', '
                name = constraint.name + self.html.anchor("cs-%s" % constraint.name)
                rows.append((name, columns))
            text.append(self.html.table(title,("Constraint name","Columns"), rows))
        # print table options
        title = "Options:" + self.html.anchor("t-opt")
        rows = []
        rows.append(("Tablespace", table.tablespace_name))
        rows.append(("Index Organized", table.index_organized))
        rows.append(("Generated by Oracle", table.secondary))
        rows.append(("Clustered", table.clustered))
        if table.clustered == 'Yes':
            rows.append(("Cluster", table.cluster_name))
        rows.append(("Nested", table.nested))
        rows.append(("Temporary", table.temporary))
        headers = "Option","Settings"
        text.append(self.html.table(title, headers, rows))
        # print indexes
        if table.indexes:
           title = "Indexes:" + self.html.anchor("t-ind")
           rows = []

           for index in table.indexes:
               columns = ''
               for i in  range(len(index.columns)):
                    columns = columns + self.html.href_to_column(index.columns[i+1],table.name, index.columns[i+1])
                    if i+1 != len(index.columns):
                        columns = columns + ', '
               name = index.name + self.html.anchor("ind-%s" % index.name)
               rows.append((name, index.type, index.uniqueness, columns, self.ddlSourceHref(index.name)))
           headers = "Index Name", "Type", "Unuqueness","Columns", 'DDL script'
           text.append(self.html.table(title, headers, rows))

        # print list of tables with references to this table
        if table.referenced_by:
           title = "Referenced by:" + self.html.anchor("t-refs")
           rows = []
           for table_name, constraint_name in table.referenced_by:
               constraint_name = self.html.href_to_constraint(constraint_name, table_name, constraint_name)
               table_name = self.html.href_to_table(table_name)
               rows.append((table_name, constraint_name))
           headers = "Table", "Constraint"
           text.append(self.html.table(title, headers, rows))

        # print triggers
        if table.triggers:
            text.append(self.html.heading("Triggers",3))
            text.append(self.html.anchor("t-trgs"))
            for trigger in table.triggers:
                text.append(self._htmlizeTrigger(trigger))

        # print partitions
        if table.tab_partitions:
            text.append(self.html.heading("Partitions", 3))
            text.append(self.html.anchor("t-parts"))
            headers = ["Partition name", "Position", "Tablespace name", "High value"]
            rows = []
            for partition in table.tab_partitions:
                rows.append([partition.partition_name, str(partition.partition_position),
                            partition.tablespace_name, str(partition.high_value)])
            text.append(self.html.table(None, headers, rows))

        # dependencies
        text.append(self._printDependencies(table.name))

        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "table-%s.html" % table.name)
        self._write(''.join(text), file_name)


    def _print_view(self, view):
        "print view page"
        # create header and context bar
        text = []
        text.append(self.html.page_header("View-%s" % view.name))
        local_nav_bar = []
        local_nav_bar.append(("Description", "v-descr"))
        local_nav_bar.append(("Columns", "v-cols"))
        local_nav_bar.append(("Query", "v-query"))
        local_nav_bar.append(("Constraints", "v-cc"))
        local_nav_bar.append(("Triggers", "v-trgs"))
        if (self._haveDependencies(view.name)):
            local_nav_bar.append(("Dependencies", "deps"))
        text.append(self.html.context_bar(local_nav_bar))
        text.append(self.html.heading(view.name, 2))
        # print comments
        if view.comments:
            text.append(self.html.heading("Description:",3) + self.html.anchor("v-descr"))
            text.append(self.html.p(self.html._quotehtml(view.comments)))
        text.append(self.ddlSourceHref(view.name))
        #print columns
        rows = []
        for i in range(len(view.columns)):
            column = view.columns[i+1]
            # add entry to doc index
            self._add_index_entry(column.name, self.html.href_to_view_column(column.name, view.name, column.name), \
                                  "column of of view %s" % view.name)
            rows.append((column.name+self.html.anchor('col-%s' % column.name), column.data_type, column.nullable,\
                         column.insertable, column.updatable, column.deletable, column.comments))
        headers = "Name", "Type", "Nullable","Insertable","Updatable", "Deletable", "Comment"
        text.append(self.html.table("Columns" + self.html.anchor('v-cols'), headers, rows))
        # print query
        text.append(self.html.heading("Query:",3) + self.html.anchor("v-query"))
        self.syntaxHighlighter.setStatement(view.text)
        self.syntaxHighlighter.parse()
        text.append(self.html.pre(self.syntaxHighlighter.getHeader()))
        text.append(self.html.pre(self.syntaxHighlighter.getOutput()))
        # print constraints
        if view.constraints:
            title = "Constraints: %s" % self.html.anchor("v-cc")
            rows = []
            for constraint in view.constraints:
                rows.append((constraint.name + self.html.anchor("cs-%s" % constraint.name),constraint.type))
            text.append(self.html.table(title, ("Constraint Name","Type"), rows))

        # print triggers
        if view.triggers:
            text.append(self.html.heading("Triggers",3))
            text.append(self.html.anchor("v-trgs"))
            for trigger in view.triggers:
                text.append(self._htmlizeTrigger(trigger))

        # dependencies
        text.append(self._printDependencies(view.name))

        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "view-%s.html" % view.name)
        self._write(''.join(text), file_name)


    def _print_mview(self, mview):
        " print materialized view"
        text = []
        text.append(self.html.page_header("MView-%s" % mview.name))
        local_nav_bar = []
        local_nav_bar.append(("Description", "v-descr"))
        local_nav_bar.append(("Columns", "v-cols"))
        local_nav_bar.append(("Query", "v-query"))
        local_nav_bar.append(("Constraints", "v-cc"))
        local_nav_bar.append(("Triggers", "v-trgs"))
        if (self._haveDependencies(mview.name)):
            local_nav_bar.append(("Dependencies", "deps"))
        text.append(self.html.context_bar(local_nav_bar))
        text.append(self.html.heading(mview.name, 2))

        th = ['Container', 'Updatable']
        container = self.html.href_to_table(mview.container)
        td = [(container, mview.mv_updatable)]
        text.append(self.html.table(None, th, td))
        # print comments
        if mview.comments:
            text.append(self.html.heading("Description:",3) + self.html.anchor("v-descr"))
            text.append(self.html.p(self.html._quotehtml(mview.comments)))
        text.append(self.ddlSourceHref(mview.name))
        #print columns
        rows = []
        for i in range(len(mview.columns)):
            column = mview.columns[i+1]
            # add entry to doc index
            self._add_index_entry(column.name, self.html.href_to_view_column(column.name, mview.name, column.name), \
                                  "column of of view %s" % mview.name)
            rows.append((column.name+self.html.anchor('col-%s' % column.name), column.data_type, column.nullable,\
                         column.insertable, column.updatable, column.deletable, column.comments))
        headers = "Name", "Type", "Nullable","Insertable","Updatable", "Deletable", "Comment"
        text.append(self.html.table("Columns" + self.html.anchor('v-cols'), headers, rows))
        # print query
        text.append(self.html.heading("Query:",3) + self.html.anchor("v-query"))
        self.syntaxHighlighter.setStatement(mview.query)
        self.syntaxHighlighter.parse()
        text.append(self.html.pre(self.syntaxHighlighter.getHeader()))
        text.append(self.html.pre(self.syntaxHighlighter.getOutput()))
        # print constraints
        if mview.constraints:
            title = "Constraints:" + self.html.anchor("v-cc")
            rows = []
            for constraint in mview.constraints:
                rows.append((constraint.name + self.html.anchor("cs-%s" % constraint.name),constraint.type))
            text.append(self.html.table(title, ("Constraint Name","Type"), rows))

        # print triggers
        if mview.triggers:
            text.append(self.html.heading("Triggers",3))
            text.append(self.html.anchor("v-trgs"))
            for trigger in mview.triggers:
                text.append(self._htmlizeTrigger(trigger))

        # dependencies
        text.append(self._printDependencies(mview.name))

        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "mview-%s.html" % mview.name)
        self._write(''.join(text), file_name)


    def _print_procedure(self, procedure):
        "print procedure page"
        # create header and context bar
        text = []
        text.append(self.html.page_header("Procedure-%s" % procedure.name))
        local_nav_bar = []
        local_nav_bar.append(("Arguments", "p-args"))
        local_nav_bar.append(("Source", "p-src"))
        if (self._haveDependencies(procedure.name)):
            local_nav_bar.append(("Dependencies", "deps"))
        text.append(self.html.context_bar(local_nav_bar))
        text.append(self.html.heading(procedure.name, 2))

        title = "Arguments:" + self.html.anchor("p-args")
        headers = "Name", "Data Type", "Default Value", "In/Out"
        rows = []
        for argument in procedure.arguments:
            if argument.default_value:
                _default_value = argument.default_value
            else:
                _default_value = ""
            row = argument.name, argument.data_type, self.html._quotehtml(_default_value), argument.in_out
            rows.append(row)
        text.append(self.html.table(title, headers, rows))
        text.append(self.ddlSourceHref(procedure.name))
        text.append(self.html.heading("Source", 2))
        text.append(self.html.anchor("p-src"))
        _src = []
        for line in procedure.source.source:
            _src.append('%s: %s' % (rjust(str(line.line_no),6), line.text))
        self.syntaxHighlighter.setStatement(''.join(_src))
        self.syntaxHighlighter.parse()
        text.append(self.html.pre(self.syntaxHighlighter.getHeader()))
        text.append(self.html.pre(self.syntaxHighlighter.getOutput()))

        # dependencies
        text.append(self._printDependencies(procedure.name))

        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "procedure-%s.html" % procedure.name)
        self._write(''.join(text), file_name)


    def _print_function(self, function):
        "print function page"
        # create header and context bar
        text = []
        text.append(self.html.page_header("Function - %s returns %s" % (function.name, function.return_data_type)))
        local_nav_bar = []
        local_nav_bar.append(("Arguments", "f-args"))
        local_nav_bar.append(("Source", "f-src"))
        if (self._haveDependencies(function.name)):
            local_nav_bar.append(("Dependencies", "deps"))
        text.append(self.html.context_bar(local_nav_bar))
        text.append(self.html.heading(function.name, 2))
        text.append(self.ddlSourceHref(function.name))

        title = "Arguments:" + self.html.anchor("f-args")
        headers = "Name", "Data Type", "Default Value", "In/Out"
        rows = []
        for argument in function.arguments:
            if argument.default_value:
                _default_value = argument.default_value
            else:
                _default_value = ""
            row = argument.name, argument.data_type, self.html._quotehtml(_default_value), argument.in_out
            rows.append(row)
        text.append(self.html.table(title, headers, rows))
        text.append(self.html.heading("Returns:",3) + function.return_data_type)
        text.append(self.html.heading("Source", 2) + self.html.anchor("f-src"))
        _src = []
        for line in function.source.source:
            _src.append(rjust(str(line.line_no),6) + ": " +  line.text)
        self.syntaxHighlighter.setStatement(''.join(_src))
        self.syntaxHighlighter.parse()
        text.append(self.html.pre(self.syntaxHighlighter.getHeader()))
        text.append(self.html.pre(self.syntaxHighlighter.getOutput()))

        # dependencies
        text.append(self._printDependencies(function.name))

        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "function-%s.html" % function.name)
        self._write(''.join(text), file_name)


    def _print_java_source(self, java_source):
        "print function page"
        # create header and context bar
        text = []
        text.append(self.html.page_header("Source of %s Java class" % java_source.name))
        local_nav_bar = []
        text.append(self.html.context_bar(local_nav_bar))
        text.append(self.html.heading('Java source: %s' % java_source.name, 2))

        rows=[]
        _src = []
        for line in java_source.source:
            _src.append(rjust(str(line.line_no),6) + ": ")
            # in java source empty string is None, so need to check before adding text
            if line.text:
                _src.append(line.text)
            #_src.append('\n')
        text.append(self.html.pre(self.html._quotehtml(''.join(_src))))

        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "java-source-%s.html" % java_source.name.replace("/", "-"))
        self._write(''.join(text), file_name)


    def _print_symbol_index_page(self):
        debug_message('print symbols index page')
        text = []
        text.append(self.html.page_header("Schema Objects Index"))
        local_nav_bar = []

        keys = self.index.keys()
        keys.sort()
        letter = ""
        for key in keys:
            if (key[:1] != letter):
                letter = key[:1]
                local_nav_bar.append((letter,letter))
        text.append(self.html.context_bar(local_nav_bar))

        letter = ""
        for key in keys:
            if (key[:1] != letter):
                letter = key[:1]
                text.append(self.html.heading(letter, 3) + self.html.anchor(letter))
            for entry in self.index[key]:
                text.append('%s %s<br/>' % entry)
        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "symbol-index.html")
        self._write(''.join(text), file_name)


    def _print_package(self, package):
        "print procedure page"
        # create header and context bar
        text = []
        text.append(self.html.page_header("Package - %s" % package.name))
        local_nav_bar = []
        local_nav_bar.append(("Package source", "p-src"))
        local_nav_bar.append(("Package body source", "p-bsrc"))
        if (self._haveDependencies(package.name)):
            local_nav_bar.append(("Dependencies", "deps"))
        text.append(self.html.context_bar(local_nav_bar))
        text.append(self.html.heading(package.name, 2))
        text.append(self.ddlSourceHref(package.name))
        title = self.html.heading("Package source", 2) + self.html.anchor("p-src")
        _src = []
        for line in package.source.source:
            _src.append(rjust(str(line.line_no),6) + ": " +  line.text)

        self.syntaxHighlighter.setStatement(''.join(_src))
        self.syntaxHighlighter.parse()
        text.append(title)
        text.append(self.html.pre(self.syntaxHighlighter.getHeader()))
        text.append(self.html.pre(self.syntaxHighlighter.getOutput()))

        title = self.html.heading("Package body source", 2) + self.html.anchor("p-bsrc")
        _src = []
        if package.body_source:
            for line in package.body_source.source:
                _src.append(rjust(str(line.line_no),6) + ": " +  line.text)
            self.syntaxHighlighter.setStatement(''.join(_src))
            self.syntaxHighlighter.parse()
            text.append(title)
            text.append(self.html.pre(self.syntaxHighlighter.getHeader()))
            text.append(self.html.pre(self.syntaxHighlighter.getOutput()))

        # dependencies
        text.append(self._printDependencies(package.name))

        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "package-%s.html" % package.name)
        self._write(''.join(text), file_name)


    def _sanity_check(self):
        debug_message('print sanity check page')
        problems = False
        text = []
        text.append(self.html.page_header("Sanity Check"))
        local_nav_bar = []
        local_nav_bar.append(("FK indexes", "fk-ix"))
        local_nav_bar.append(("Invalid objects", "inv"))
        text.append(self.html.context_bar(local_nav_bar))

        text.append(self.html.heading("Sanity Check", 1))

        scheck = SchemaAnalyzer(self.cfg.connection, self.cfg.schema)
        if scheck.fk_no_indexes:
            text.append(self.html.anchor("fk-ix"))
            text.append(self.html.heading("No indexes on columns involved in foreign key constraints",2))
            text.append('''<p>You should almost always index foreign keys. The only exception is when
                        the matching unique or primary key is never updated or deleted. For
                        more information take a look on
                        <a href="http://oradoc.photo.net/ora817/DOC/server.817/a76965/c24integ.htm#2299">
                        Concurrency Control, Indexes, and Foreign Keys</a>.</p>
                        <p>The sql file which will
                        generate these indexes is <a href="fk-indexes.sql">created for you</a></p>''')

            title = '"Unindexed" foreign keys'
            headers = "Table Name", "Constraint name", "Columns"
            rows = []
            for constraint in scheck.fk_no_indexes:
                row=[]
                row.append( self.html.href_to_table(constraint.table_name))
                row.append( self.html.href_to_constraint(constraint.name, constraint.table_name, constraint.name))
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
            file_name = path.join(self.cfg.output_dir, "fk-indexes.sql")
            self._write(scheck.fk_no_indexes_sql,file_name)
            text.append(self.html.table(title,headers,rows))
            problems = True

        if len(scheck.invalids) != 0:
            problems = True
            text.append(self.html.anchor("inv"))
            text.append(self.html.heading('Invalid objects', 2))
            text.append('''<p>Invalid object does not mean a problem sometimes. Sometimes will
                    fix itself as is is executed or accessed.  But if there is an error in
                    USER_ERRORS table, you are in trouble then...</p>
                    <p>The sql file which will compile these objects is
                    <a href="compile-objects.sql">created for you</a>.</p>''')
            self._write(scheck.invalids_sql, path.join(self.cfg.output_dir, 'compile-objects.sql'))
            invalids = scheck.invalids
            for i in invalids:
                if i[1] == 'PACKAGE' or i[1] == 'PACKAGE BODY':
                    i[0] = self.html.href_to_package(i[0])
                if i[1] == 'PROCEDURE':
                    i[0] = self.html.href_to_procedure(i[0])
                if i[1] == 'FUNCTION':
                    i[0] = self.html.href_to_function(i[0])
                if i[1] == 'VIEW':
                    i[0] = self.html.href_to_view(i[0])
                if i[1] == 'TRIGGER':
                    for j in self.cfg.schema.triggers:
                        if j.name == i[0]:
                            i[0] = self.html.href_to_trigger(i[0], j.table_name, i[0], self.triggerAnchorType(j))
                            break
                i[2] = self.html._quotehtml(i[2])
            text.append(self.html.table('Invalids', ['Object name', 'Type', 'Error', 'At line'], invalids))

        if problems == False:
            # no checks
            text.append(self.html.p('No known problems.'))
        text.append(self.html.page_footer())
        file_name = path.join(self.cfg.output_dir, "sanity-check.html")
        self._write(''.join(text), file_name)


    def _write(self, text, file_name):
        # write file to fs
        debug_message("debug: writing file %s" % file_name)
        f = open(file_name, 'w')
        f.write(text)
        f.close()


    def _add_index_entry(self, key , link, description):
        # add new entry to symbol index
        t = self.index.get(key)
        if not t:
            self.index[key] = t = []
        t.append((link, description))


    def _print_common_pages(self):
        # print index.html, nav.html and main.html
        text = self.html._index_page(self.cfg.name)
        file_name = path.join(self.cfg.output_dir, "index.html")
        self._write(text, file_name)
        text = self.html._global_nav_frame(self.cfg.name)
        file_name = path.join(self.cfg.output_dir, "nav.html")
        self._write(text, file_name)
        # er diagram
        imgname = None
        if self.dotEngine.haveDot:
            erdDict = {}
            for table in self.cfg.schema.tables:
                refs = []
                if table.referential_constraints:
                    for ref in table.referential_constraints:
                        refs.append(ref.r_table)
                erdDict[table.name] = refs
            imgname = self.dotEngine.fileGraphDict(erdDict)
            if imgname != None:
                try:
                    f = file(path.join(self.cfg.output_dir, 'main.map'), 'r')
                    text = self.html.imgMap('mainmap', f.read())
                    f.close()
                    remove(path.join(self.cfg.output_dir, 'main.map'))
                except IOError:
                    text = ''
                    print 'error reading main.map GraphViz file'
                imgname = text + self.html.img(imgname, htmlMap='mainmap', cssClass='erd')

        text = self.html._main_frame(self.cfg.name, self.cfg.desc, self.syntaxHighlighter.highlight, imgname)
        file_name = path.join(self.cfg.output_dir, "main.html")
        self._write(text, file_name)


    def _print_index_frame(self, header, item_list, file_name):
        # generic procedure to print index frame on left side
        # excpects:
        #          header    - title string, i.e "Tables"
        #          item_list - list of names with html links
        #          file_name - relative file name
        debug_message('index frame for %s' % header)
        text = []
        text.append(self.html.frame_header(header))
        text.append(self.html.href('nav.html', 'Categories'))
        for row in item_list:
            text.append(row)
        text.append(self.html.frame_footer())
        #java sources contain simbol / inside name, in file_names should be replaced with "-"
        f_name = path.join(self.cfg.output_dir, file_name.replace("/","-"))
        self._write(''.join(text), f_name)


    def _print_list_page(self, title, ht_table, file_name):
        # print list pages
        debug_message('print %s list page' % title)
        text = self.html.page_header(title)
        text = text + self.html.context_bar( None)
        text = text + ht_table
        text = text + self.html.page_footer()

        file_name = path.join(self.cfg.output_dir, file_name.replace("/", "-"))
        self._write(text, file_name)


    def _haveDependencies(self, key):
        return self.cfg.schema.dependencies.has_key(key)

    def _printDependencies(self, key):
        """ Prints the dependecy table for given key/object """
        if (self._haveDependencies(key)):
            return self.html.table("Dependencies" + self.html.anchor('deps'),
                                    ['Referenced Owner', 'Referenced Name',
                                     'Referenced Link', 'Referenced Type',
                                     'Dependency Type'],
                                    self.cfg.schema.dependencies[key])
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

