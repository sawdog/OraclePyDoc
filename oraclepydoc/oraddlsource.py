""" Create a DDL script of the objects """


import cx_Oracle
import os.path
import os
import time


class OraDDLSource(object):
    """ Obtaining the DDL script depends on the DBMS_METADATA package.
        So it's limited only for version 9 and greater and for users
        with EXECUTE privilege on this package.
        When it cannot be found there is only a message written. """

    def __init__(self, cfg):
        self.cfg = cfg
        self.connection = cfg.connection
        self.enabled = self.checkForMetadata()
        self.fname = None
        self.directory = os.path.join(cfg.output_dir, 'sql_sources')
        self.rootDir = cfg.output_dir
        self.scriptCache = {}
        if not self.mkdir(self.directory):
            self.enabled = False
        # disable DDL generators - but the previous stuff
        # is required to be set
        if not cfg.allowDDL:
            self.enabled = False

    def mkdir(self, dirname):
        if os.path.isdir(dirname):
            return True
        try:
            os.mkdir(dirname)
            return True
        except:
            return False
            print 'WARNING: cannot create directory %s' % outputDir
            print 'WARNING: DDL script creation is disabled'

    def checkForMetadata(self):
        print 'Checking for DDL scripts creating availability'
        res = self.query("""select count(1)
                        from all_tab_privs
                        where table_name = 'DBMS_METADATA'
                            and privilege = 'EXECUTE'
                            --and grantee in ('PUBLIC', 'S0')
                            """)
        if res[0][0] > 0:
            print 'DBMS_METADATA found\n'
            return True
        print 'WARNING: No EXECUTE grant on DBMS_METADATA (>8) or feature '\
                'disabled (8)'
        return False

    def getDDLScript(self, objType, objName):
        if not self.enabled or self.directory == None:
            return None
        if objName in self.scriptCache:
            return
        ownerStrip = objName.find('.')
        if ownerStrip != -1:
            splitName = objName.split('.')
            par = {'type': objType, 'name': splitName[1],
                    'schema': splitName[0]}
            sql = 'select dbms_metadata.get_ddl(:type, :name, :schema) '\
                    'from dual'
        else:
            par = {'type': objType, 'name': objName}
            sql = "select dbms_metadata.get_ddl(:type, :name) from dual"
        try:
            # CLOBS cannot be fetchall()ed!
            cur = self.connection.cursor()
            cur.execute(sql, par)
            ddl = []
            row = cur.fetchone()
            while row:
                ddl.append(row[0].read())
                try:
                    row = cur.next()
                except StopIteration:
                    break
        except cx_Oracle.DatabaseError, e:
            print 'ERROR: DDL creation is inconsistent for: %s %s' % \
                    (par['type'], par['name'])
            print '       %s' % e.__str__()[:e.__str__().find('\n')]
            return None
        self.fname = '%s.sql' % objName.lower()
        currentDir = os.path.join(self.directory, objType.replace(' ',
            '_').lower())
        if not self.mkdir(currentDir):
            self.enabled = False
            return None
        f = file(os.path.join(currentDir, self.fname), 'w')
        f.write(''.join(ddl))
        f.write('\n/\n')
        f.close()
        strippedName = os.path.join(currentDir,
                self.fname)[len(self.rootDir) + 1:]
        self.scriptCache[objName] = strippedName
        return strippedName

    def query(self, statement, params={}):
        cur = self.connection.cursor()
        cur.execute(statement, params)
        results = cur.fetchall()
        cur.close()
        return results


# unit tests are for losers...
if __name__ == '__main__':
    c = cx_Oracle.connect('s0/asgaard')
    o = OraDDLSource(conn=c)  # , outputDir='./foo')
    print o.getDDLScript('TABLE', 'ENCODING')
    print o.getDDLScript('TABLE', 'ENCODIN')
    print o.getDDLScript('FOO', 'TABLE2')
