"""hand writing the reST elements

   Todo:  generalize the foo_label methods and href_to_foo methods.  Can look
          up the type in a mapping and have a single method for all obs.

"""

from string import join
from string import replace
import time

from rippy import RIP

hlevels = RIP.header_levels


class reSTFormatter(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.name = cfg.name
        self.notNulls = cfg.notNulls
        self.fpname = cfg.fpname

    def anchor(self, text):
        return RIP.anchor(text)

    def br(self):
        return '\n'

    def download_href(self, path, text):
        return RIP.download(path, text)

    def heading(self, text, level):
        """The heading is offset by 2 line breaks from whatever follows"""
        return RIP.header(text, level)

    def doc(self, label, text=None):
        """For Cross-referencing to documents"""
        return RIP.doc(label, text)

    def href(self, label, text=None):
        return RIP.ref(label, text)

    def i(self, text):
        return RIP.emphasis(text)

    def imgMap(self, name, content):
        # need to make the map tag output a single string.
        return '.. raw:: html \n\n  <map name="%s">%s</map>\n\n' % (name,
                content.replace('\n', ''))

    def img(self, name, htmlMap='mainmap'):
        """XXX Would like to figure out how to also write and link to image in
           a file, so we can link to it and have the image map working....

        """
        return '''.. image:: name\n'''

    def img_raw(self, url, htmlMap='mainmap', cssClass='erd'):
        """return the raw html for images that are in images."""
        return '.. raw:: html\n\n  <img class="%s" usemap="#%s" '\
                'src="./images/%s"/>' % (cssClass, htmlMap, str(url))

    def context_bar(self, local_nav_bar):
        text = []
        return join(text, '')

    def href_to_column(self, text, table_name, column_name):
        label = '%s-table-%s-col-%s' % (self.fpname, table_name, column_name)
        return self.href(label, text)

    def href_to_constraint(self, text, table_name, constraint_name):
        """Create the link to a constraint in a given table.

           XXX see the comments re: href_to_index, as they apply here::

                label = '%s-cs-%s' % (self.table_label(table_name),
                                      constraint_name)

        """
        label = '%s-constraints' % self.table_label(table_name)
        return self.href(label, text)

    def href_to_trigger(self, text, table_name, trigger_name, trigger_type):
        """Create the link to a trigger in a given table.

           XXX see the comments re: href_to_index, as they apply here::

                label = '%s-%s-%s-trg-%s' % (self.fpname, trigger_type,
                            table_name, trigger_name)

        """
        label = '%s-triggers' % self.table_label(table_name)
        return self.href(label, text)

    def href_to_index(self, text, table_name, index_name):
        """In the reST pages, the index is listed in a table.

           XXX i currently do not know how to make anchors inside reST table
           rows, so we just link to an anchor atop the indexes table.  If this
           changes, then this method should construct the lable by::

                label = '%s-index-%s' % (self.table_label(table_name),
                                         index_name)

        """
        label = '%s-index-table' % self.table_label(table_name)
        return self.href(label, text)

    def href_to_table(self, name):
        """tables are *real* rst files - so we link to by ref or
           the rst file name returned by table_label

        """
        return self.href('%s-' % self.fpname + self.table_label(name), name)

    def table_label(self, name):
        """Generate common label to use to link to tables."""
        return '%s' % name

    def href_to_synonym(self, name):
        """synonyms are not *real* rst files - so we do what?
           punt?  link to by ref or
           the rst file name returned by table_label

        """
        return self.href('%s-' % self.fpname + self.synonym_label(name), name)

    def synonym_label(self, name):
        """Generate common label to use to link to synonyms."""
        return '%s' % name

    def href_to_sequence(self, name):
        return self.href('%s-' % self.fpname + self.sequence_label(name),
                name)

    def sequence_label(self, name):
        """Generate common label to use to link to sequences."""
        return '%s' % name

    def href_to_view(self, name):
        """Views are *real* rst files like tables - so we link to by ref or
           the rst file name returned by view_label

        """
        return self.href('%s-' % self.fpname + self.view_label(name), name)

    def view_label(self, name):
        """Generate common label to use to link to views."""
        return '%s' % name

    def href_to_materialized_view(self, name):
        """MaterializedViews are *real* rst files like tables and views - so we
           link to by ref or the rst file name returned by mview_label

        """
        return self.href('%s-' % self.fpname + \
                self.materialized_view_label(name), name)

    def materialized_view_label(self, name):
        """Generate common label to use to link to materialized views."""
        return '%s' % name

    def href_to_procedure(self, name):
        return self.href('%s-' % self.fpname + self.procedure_label(name),
                name)

    def procedure_label(self, name):
        """Generate common label to use to link to procedures"""
        return '%s' % name

    def href_to_function(self, name):
        return self.href('%s-' % self.fpname + self.function_label(name),
                name)

    def function_label(self, name):
        """Generate common label to use to link to functions"""
        return '%s' % name

    def href_to_package(self, name):
        return self.href('%s-' % self.fpname + \
                self.package_label(name), name)

    def package_label(self, name):
        """Generate common label to use to link to packages"""
        return '%s' % name

    def href_to_view_column(self, text, view_name, column_name):
        label = '%s-view-%s-col-%s' % (self.fpname, view_name, column_name)
        return self.href(label, text)

    def href_to_java_source(self, name):
        return self.href('%s-' % self.fpname + \
                self.java_source_label(name), name)

    def java_source_label(self, name):
        return '%s' % name.replace('/', '-')

    def href_to_job(self, name):
        return self.href('%s-jobs-%s' % (self.fpname, name), name)

    def href_to_type(self, name):
        """Generate the href for a type in the dependencies....

        """
        return self.href('%s-' % self.fpname + self.type_label(name), name)

    def type_label(self, name):
        """Generate common label to use to link to type."""
        return '%s' % name

    def operator_label(self, name):
        """Generate common label to use to link to operator."""
        return '%s' % name

    def href_to_library(self, name):
        """Generate the href for a library....

        """
        return self.href('%s-' % self.fpname + self.library_label(name), name)

    def library_label(self, name):
        """Generate common label to use to link to library."""
        return '%s' % name

    def page_footer(self):
        return ''

    def page_header(self, text):
        """page header for a typical rest page is an anchor to link back to
           the page from other pages...

           XXX first few passes at generalizing this, we'll presume we're taking
           some string that we just append the fpname to::

             %s-%s % (self.fpname, text)

        """
        return '.. _%s:\n\n' % self.header_link(text)

    def header_link(self, text):
        """generate the link to the page header generated by::

            def page_header(self, text)

        """
        return '%s-%s' % (self.fpname, text)

    def pre(self, text):
        return '``%s``' % text

    def p(self, text):
        """Offset's with 2 line breaks...."""
        return '%s\n\n' % text

    def table(self, name, headers, rows, width=None, anchor=None,
            heading_level=3):
        """The 'columns need to be as 'wide' as the widest
           data element within a cell.

           So we need to run through all the elements first, find the
           'widest' element and then padd everything to match that.

           If anchor is passed, an anchor to the table is created above
           the name section header.

           heading_level is the level of the name/title of the table being
           created.

        """
        return RIP.table(name, headers, rows, anchor, heading_level)

    def _index_page(self, name):
        return ''

    def _global_toc(self):
        """Global TOC is simply the toctree for main page elements of the
           documentation.

           XXX todo: do not print out toc items which do not have entries.
        """
        text = []
        text.append('\n' + self.heading('Table of Contents', 2) + '\n')
        text.append('.. toctree::\n')
        text.append('   :maxdepth: 1\n\n')
        text.append('   Tables <tables-index>\n')
        text.append('   Views <views-index>\n')
        text.append('   Materialized Views <mviews-index>\n')
        text.append('   Indexes <indexes-index>\n')
        text.append('   Constraints <constraints-index>\n')
        text.append('   Triggers <triggers-index>\n')
        text.append('   Procedures <procedures-index>\n')
        text.append('   Functions <functions-index>\n')
        text.append('   Packages <packages-index>\n')
        text.append('   Sequences <sequences-index>\n')
        text.append('   Java Sources <java-sources-index>\n')
        text.append('   Sanity Check <sanity-check>\n')
        return join(text, '')

    def _quotehtml (self, text):
        """XXX not sure what reST want's handled yet..."""
        #text = replace(text, "&", "&amp;")
        #text = replace(text, "\\", "&quot;")
        #text = replace(text, "<", "&lt;")
        #text = replace(text, ">", "&gt;")
        return text

    def _main_frame(self, name, description, highlight, imgname=None):
        """This is part of the nav.rst page in the reST formatting."""
        text = []

        highlight = highlight and 'Yes' or 'No'
        text.append(self.heading('Overivew', 2))
        text.append(self.br())
        text.append(self.p('**Description**:\n  %s' % description))
        text.append(self.p('\n**Using syntax highlighting**:\n  %s' % \
                highlight))

        text.append(self.p('\n**Oracle Encoding**:\n  %s' % self.cfg.ora_encoding))
        text.append(self.p('\n**Web Character set**:\n  %s' % self.cfg.webEncoding))

        if not self.notNulls:
            text.append(self.p('\n**Constraints**:\n  NOT NULL constraints '\
                'are skipped.  This information is kept in colums list. One '\
                'can enable its listing by `--not-nulls` option when '\
                'generating these docs.\n'))

        # create a note for DDL script dependencies...
        text.append(self.p('\n' +\
                RIP.note('Obtaining the DDL script depends on the '\
                'DBMS_METADATA package.  So this is limited only to users '\
                'with EXECUTE privilege on this package.')))
        return ''.join(text)

    def _index_frame(self, header, item_list, file_name):
        """Index frames are for items which do not have *real* .rst files to
           point to.....

         generic procedure to print index page::

                  header    - title string, i.e "Tables"
                  item_list - :ref: formatted links to items.
                  file_name - to generate an anchor to link to the index

        """
        text = []
        tappend = text.append
        # create the initial anchor...so other things can link back to it.
        hanchor = file_name.split('.')[0]
        tappend(self.anchor(hanchor))
        tappend(self.heading(header, 1))
        # now generate the toctree and options
        tappend(self.heading('Table of Contents', 2))
        for row in item_list:
            tappend(row)

        return join(text, '')

    def _toc_frame(self, header, item_list, file_name):
        """Index frame really is a toctree for the 'type' being listed.

         generic procedure to print index page::

                  header    - title string, i.e "Tables"
                  item_list - list of rst page names
                  file_name - to generate an anchor to link to the index

        on this listing, also include the tables-index

        """
        text = []
        tappend = text.append
        # create the initial anchor...so other things can link back to it.
        hanchor = file_name.split('.')[0]
        tappend(self.anchor(hanchor))
        tappend(self.br())
        tappend(self.heading(header, 1))
        text.extend([self.br(), self.br()])
        # now generate the toctree and options
        tappend(self.heading('Table of Contents', 2))
        text.extend([self.br(), self.br()])
        tappend('.. toctree::\n   :maxdepth: 1\n\n')
        # each row needs to be indented 3 spaces
        # XXX must match the indendtation level of :maxdepth: above
        for row in item_list:
            tappend('   %s\n' % row)

        return join(text, '')
