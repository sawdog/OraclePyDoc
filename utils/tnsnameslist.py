""" Try to find tnsnames.ora and print its content.

OK, I know it's an ugly code but I needed to write it
in 20 minutes and I don't want to waste a time with
rewritting it...
"""

__author__ = 'Petr Vanek <petr@yarpen.cz>'

import sys
import os
import getopt


def usage():
    """ small help """
    print \
"""
Simple TNSNAMES parser and founder

usage: python %s [-h|--help] [filename]

   -h --help   prints this help
   filename    optional filename with tnsnames entries.

It can found some tnsnames.ora itsels if you don't specify the filename.
This automatic search walks through your environment variables TNS_NAMES,
ORACLE_HOME, then it search your PATH for it. All paths containing string
'SAMPLE' are ignored.
""" % sys.argv[0]


def walk( root, recurse=0, pattern='*', return_folders=0 ):
    """ Recursive directory walking.
    Simplified function. Original author Robin Parmar
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52664"""
    import fnmatch, os, string
    
    # initialize
    result = []

    # must have at least root folder
    try:
        names = os.listdir(root)
    except os.error:
        print 'os.error'
        return result

    # check each file
    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))

        # grab if it matches our pattern and entry type
        if fnmatch.fnmatch(name, pattern):
            if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
                result.append(fullname)
            continue
                
        # recursively scan other folders, appending results
        if recurse:
            if os.path.isdir(fullname) and not os.path.islink(fullname) and fullname.upper().find('SAMPLE') == -1:
                result = result + walk( fullname, recurse, pattern, return_folders )
            
    return result


class TnsNames:
    """ Simple tnsnames.ora parser and printer """

    def __init__(self, fname):
        """ Strip out whitespaces, comments and blank lines """
        try:
            f = file(fname, 'r')
        except IOError:
            print 'FATAL ERROR: Cannot open %s' % fname
            sys.exit(1)

        lines = []
        parens = 0
        # switch off comments and whitespaces
        for line in f:
            l = line.strip()
            comm = l.find('#')
            if comm != -1:
                l = l[:comm] 
            lines.append(l)
        tns = ' '.join(lines).lower()
        self.tns = tns.replace(' ', '')


    def parse(self):
        """ Nicer grep -v -e '^ ' -e'^\t' -e'^$' -e '^#' -e'^)' ./tnsnames.ora |
        awk '{sub("=", "", $1); print $1}' ;)
        P.S.: ;) is not shell sequence
        """
        level = 0
        ret = {}
        out = ''
        stuff = False
        # range is here bacouse of substring handling
        for i in range(len(self.tns)):
            if self.tns[i] == '(':
                level += 1
                continue
            if self.tns[i] == ')':
                level -= 1
                continue
            if level == 1 and stuff == False:
                out = out.replace('=','')
                ret[out] = (self._getStuff(self.tns[i:], '(host='), 
                            self._getStuff(self.tns[i:], '(port='),
                            self._getStuff(self.tns[i:], '(protocol='),
                            self._getStuff(self.tns[i:], '(sid='))
                out = ""
                stuff = True
            if level == 0:
                out += self.tns[i]
                stuff = False
        return ret


    def _getStuff(self, str, begin):
        """ Get substring from 'begin' to ')' interval """
        start = str.find(begin)
        substr = str[start:]
        end = substr.find(')')
        return substr[:end].replace(begin, '')


def getWinRegistry():
    if os.name != 'nt':
        return None
    print 'Searching Windows registry for TNS_NAMES'

    try:
        import win32api, win32con
    except ImportError:
        print """
        Cannot load win32 extension for Python. Please install it.
        https://sourceforge.net/projects/pywin32/
        OK, it proves you cannot run this script on UN*X. Take it
        easy - it's needless because you can edit ORACLE_HOME easy.
        """
        return None
    try:
        homekey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,
                                        'SOFTWARE\\ORACLE',
                                        0, win32con.KEY_READ)
        tns, aType = win32api.RegQueryValueEx(homekey, 'TNS_NAMES')
        return tns
    except:
        pass 
    return None
        
 
def getActualTns():
    """ Search env variables. Then path """
    print 'Automatic TNSNAMES searching'

    try:
        tnspath = os.environ['TNS_NAMES']
        print 'Using %s' % tnspath
        return os.path.join(tnspath, 'tnsnames.ora')
    except KeyError:
        print 'TNS_NAMES variable not found'
    try:
        tnspath = os.environ['ORACLE_HOME']
        print 'Using %s' % tnspath
        return os.path.join(tnspath, 'network', 'admin', 'tnsnames.ora')        
    except KeyError:
        print 'ORACLE_HOME variables not found'

    reg = getWinRegistry()
    if  reg != None:
        print 'Found %s in registry' % reg
        return reg

    print 'Searching PATH for the fist tnsnames.ora occurence'
    for i in os.environ['PATH'].split(';'):
        print i
        r = walk(i, 1, 'tnsnames.ora')
        if len(r) != 0:
            return r[0]
    return None

    
if __name__ == '__main__':
    print 'use -h parameter to get small help'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.error, e:
        # print help information and exit:
        usage()
        sys.exit(1) 
    
    for opt, value in opts:
        if opt in ('-h', '--help'):
            # print help information and exit:
            usage()
            sys.exit() 

    if len(args) == 1:
        fname = args[0]
    else:
        fname = getActualTns()
    
    if fname == None:
        print 'No auto-tns found.'
        sys.exit(1)

    t = TnsNames(fname)
    tns = t.parse()
    print '\ntnsnames: %s' % fname
    print '\n%15s\t%25s:%4s\t%5s\t%8s' % ('world', 'host', 'port', 'net', 'SID')
    print 80 * '-'
    for i in tns.keys():
        print '%15s\t%25s:%4s\t%5s\t%8s' % (i, tns[i][0], tns[i][1], tns[i][2], tns[i][3])
    
