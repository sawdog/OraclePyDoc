"""Configure attributes packed together"""

import os
from os.path import join
from string import lower
import sys

class OSDConfig(object):
    """Configure attributes packed together"""

    def __init__(self):
        """ Default values if used without of orachemadoc.py """
        #  text string to display "project"/schema name
        self.name = None
        #   variable used for turning on debug messages
        self.verbose_mode = False
        #  directory to store outputs
        self.output_dir = '.'
        #  Allow to generate DLL scripts
        self.allowDDL = True
        #  if specified, restrict export to dia only for table names included in file
        self.dia_conf_file = None
        self.dia_file_name = 'default.dia'
        #  if true then sources will have syntax highlighting
        self.syntaxHighlighting = False
        #  path to css (default here)
        self.csspath = join(sys.path[0], 'css')
        #  file for html doc css styles
        self.css = 'oraschemadoc.css'
        #  decription
        self.desc = None
        #  package bodies
        self.pb = False
        #  take NOT NULL constraints. False = don't take NOT NULL constraints
        self.notNulls = False
        #  list of the usernames.
        self.useOwners = False
        self.owners = []
        self.currentUser = ''
        #  DB connection
        self.connection = None
        #  DB attributes
        self.encoding = None

        # we will always encode output as utf-8
        # regardless what the db encoding is, as it's effectively
        # for the web.
        self.webEncoding = 'utf8'
        #  internals
        self.dictionary = None
        self.schema = None

    @property
    def fpname(self):
        """Used if there is a need to differentiate files between the various
           projects, e.g.::

               image names which might not be unique

           By convention, this is going to be the last part of the output_dir
           - which **should** be the schema name for the doc run.

        """
        return os.path.split(self.output_dir)[-1]
