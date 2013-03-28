#!/usr/bin/env python

""" Generates pluggable information about Oracle schema objects """

import argparse
import os
import shutil
from string import upper
from sys import exit

import cx_Oracle

from oraclepydoc.formatter.html import HTMLFormatter
from oraclepydoc.writer.rest import reSTWriter
from oraclepydoc.oracleencoding import OracleNLSCharset
from oraclepydoc.osdconfig import OSDConfig
from oraclepydoc.orasdict import OraSchemaDataDictionary
from oraclepydoc.oraschema import  OracleSchema
from oraclepydoc.oraverbose import debug_message
from oraclepydoc.oraverbose import set_verbose_mode


def main():
    """parse the command line args and run the formatting/writing of
       the documentation

    """
    parser = argparse.ArgumentParser(description='Parse command line args.')

    # add all the possible arguments we expect to handle via the cli
    parser.add_argument('-u', dest='username', action='store', required=True,
            help='db schema')
    parser.add_argument('-p', dest='password', action='store', required=True,
            help='Password for the db schema')
    parser.add_argument('-t', dest='tsn', action='store', required=True,
            help='Network TSN alias')
    parser.add_argument('-o', dest='output_dir', action='store', required=True,
            help='Output directory for doc generation, for sphinx '\
                    'documentation this is the same name as the schema '\
                    'name so that links can be made between schemas.')
    parser.add_argument('-n', dest='name', action='store', required=False,
            default=False, help='DB Project name')
    parser.add_argument('-v', dest='verbose', action='store_true',
            default=False, help='Display verbose "build" text when running.')
    parser.add_argument('-s', dest='syntax_highlighting', action='store_true',
            default=False,
            help='When formatting as html, turn on syntax highlighting.')
    parser.add_argument('--css', dest='css', action='store',
            help='When formatting as html, path to custom css file')
    parser.add_argument('--noddl', dest='noddl', action='store_true',
            default=False, help='Diasble ddl generation')
    parser.add_argument('--dia', dest='dia', action='store_true',
            default=False, help='Enable dia uml output')
    parser.add_argument('--dia_conf_file', dest='dia_conf_file',
            action='store', help='Path to the dia conf table file.  Only '\
                    'create dia diagrams of tables in conf file')
    parser.add_argument('--desc', dest='description', action='store',
            help='Project description added to the documentation index')
    parser.add_argument('--dia-table-list', dest='dia-table-list',
            action='append', help='Filename for dia table lists')
    parser.add_argument('--not-nulls', dest='notnulls', action='store_true',
            default=False, help='Do not Write out the not null contraints')
    parser.add_argument('--pb', dest='pb', action='store_true',
            default=False, help='Do not write out the package bodies')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--html', dest='html', action='store_true',
            default=False, help='Format output as javadoc html files')
    group.add_argument('--rest', dest='rest', action='store_true',
            default=False, help='Format output as reST files')
    group.add_argument('--xml-file', dest='xml', action='store',
            help='Generate output into xml file')

    # create global config file - hanger passed around to various apps...
    # bleagh - but how it is in first fork....
    cfg = OSDConfig()

    pargs = parser.parse_args()

    # username/schema
    username = pargs.username

    # do we want to generate ddl?
    cfg.allowDDL = not pargs.noddl

    # Just stick these as they are....
    cfg.dia_conf_file = cfg.dia_conf_file
    name = pargs.name
    cfg.name = name and name or upper(username)
    cfg.notNulls = pargs.notnulls
    cfg.pb = pargs.pb
    cfg.xml_file = pargs.xml
    verbose = cfg.verbose = pargs.verbose
    set_verbose_mode(verbose)

    # make sure the dia conf file exists if set.
    if cfg.dia_conf_file:
        if not os.path.exists(cfg.cfg.dia_conf_file):
            cfg.dia_conf_file = None

    css = pargs.css
    if css:
        if not os.path.exists(os.path.join(cfg.csspath, css)):
            msg = '\nWARNING: %s doesn\'t exists. Using default instead.\n' % \
                    value
            debug_message(msg)
        else:
            cfg.css = css

    #if opt == '--schema':
    #    cfg.useOwners = True
    #    if len(value) > 0:
    #        cfg.owners = value.split(',')

    # output dir is the dir the directory is created - based on::
    # db.schema_name format - so /tmp/foo.username
    output_dir = os.path.join(os.path.abspath(pargs.output_dir),
                              '%s.%s' % (pargs.tsn, username))
    cfg.output_dir = output_dir

    # check if output_dir exsits, if not try to create one.
    if os.access(cfg.output_dir, os.F_OK) != 1:
        try:
            os.makedirs(cfg.output_dir)
        except os.error, e:
            print 'ERROR: Cannot create directory ', cfg.output_dir
            exit(2)
    else:
        # if directory exists see if its writable
        if os.access(cfg.output_dir, os.W_OK) != 1:
            print 'ERROR: Cannot write into directory ', cfg.output_dir
            exit(2)

    connect_string = '%s/%s' % (pargs.username,
            pargs.password) + '@' + '%s' % pargs.tsn
    try:
        cfg.connection = cx_Oracle.connect(connect_string)
    except cx_Oracle.DatabaseError, e:
        print e
        exit(2)

    # XXX effectively also the schema
    cfg.currentUser = connect_string[:connect_string.find('/')].upper()

    # know encoding we will use
    oraenc = OracleNLSCharset()
    encoding = oraenc.getClientNLSCharset()
    cfg.ora_encoding = oraenc.getOracleNLSCharacterset(cfg.connection)
    if encoding == None:
        encoding = oraenc.getPythonEncoding(cfg.ora_encoding)
    else:
        encoding = oraenc.getPythonEncoding(encoding)

    cfg.encoding = encoding
    debug_message('Using codec: %s' % cfg.encoding)
    debug_message('HTML encoding: %s\n' % cfg.webEncoding)

    # make sure that the name and desc. are encoded
    if cfg.desc != None:
        cfg.desc = cfg.desc.encode(encoding)

    cfg.name = cfg.name.encode(encoding)

    cfg.dictionary = OraSchemaDataDictionary(cfg)
    cfg.schema = OracleSchema(cfg)

    if pargs.html:
        cfg.syntaxHighlighting = pargs.syntax
        # all the magic is in this formatter's __init__ for now
        HTMLFormatter(cfg)

    if pargs.rest:
        # all the magic is in this writer's __init__ for now
        reSTWriter(cfg)

        # since we have all the image maps in rest, we have to generate things
        # with raw html.  Thus, we need to move all the .png files into
        # the ./images/ dir so that when docs are built, they are there...

        #image_dir = os.path.join(os.path.split(cfg.output_dir)[:-1][0],
        #        '_static')
        image_dir = os.path.join(cfg.output_dir, 'images')
        # check if image_dir exsits, if not try to create one.
        if os.access(image_dir, os.F_OK) != 1:
            try:
                os.makedirs(image_dir)
            except os.error, e:
                print 'ERROR: Cannot create directory ', image_dir
                exit(2)
        for f in os.listdir(cfg.output_dir):
            if f.endswith('.png'):
                shutil.move(os.path.join(cfg.output_dir, f),
                        '%s/%s' % (image_dir, f))

    if pargs.xml:
        writer = XMLWriter(cfg)
        write.write()

    if pargs.dia:
        writer = Diawriter(cfg)
        writer.write()


if __name__ == '__main__':
    main()
