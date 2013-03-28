""" Changing ORACLE_HOME in UN*X is easy. I wish I can change
it this way on Windows... I've tried some 3rd party utilities
with only a minor success. It messes the system a lot etc.
This script appears to do it right way and the right way is
my way so use it carefully because this program is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY...

LICENSE: GPLv2 http://www.gnu.org/licenses/gpl.html
AUTHOR: Petr Vanek, petr@yarpen.cz

Note that at the moment enver doesn't modify the active environment,
but only the registry so new command windows will see the changes.
So, if you type: 'set' after running enver you won't see any changes.
Setting os.environ wouldn't help because the script is executed in
a different shell then the host window.
"""

import sys
import getopt
import os
import string

try:
    import win32api, win32con, win32gui
except ImportError:
    print """
    Cannot load win32 extension for Python. Please install it.
    https://sourceforge.net/projects/pywin32/
    OK, it proves you cannot run this script on UN*X. Take it
    easy - it's needless because you can edit ORACLE_HOME easy.
    """
    sys.exit(1)


def isKeyOrahome(key, ix):
    """ Check if the registry key contains oracle home item """
    try:
        for i in  win32api.RegEnumValue(key, ix):
            if i == 'ORACLE_HOME':
                return True
    except:
        return False
    return False


def getAllHomes():
    " Get list with available homes "
    oracle_homes = {}
    key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,
                                'SOFTWARE\\ORACLE',
                                0, win32con.KEY_READ)
    for name, reserved, oraclass, lastwritetime in win32api.RegEnumKeyEx(key):
        try:
            homekey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,
                                            'SOFTWARE\\ORACLE\\' + name,
                                            0, win32con.KEY_READ)
            orahome, aType = win32api.RegQueryValueEx(homekey, 'ORACLE_HOME')
            orahomename, aType = win32api.RegQueryValueEx(homekey,
                                                          'ORACLE_HOME_NAME')
            oracle_homes[orahomename] = orahome
        except:
            # nothing to do here
            pass #print 'ORAHOME: ' + name + ' is not oracle home'
    return oracle_homes


def setupHome(oracle_homes, id):
    """ Setup the path """
    if not oracle_homes.has_key(id):
        print '\nError: No ORACLE_HOME "%s" found.' % str(id)
        printHomes(oracle_homes)
        sys.exit(1)
    #path = 
    print '\nSetting: %s' % oracle_homes[id]
    reg = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,
                                'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment',
                                0, win32con.KEY_ALL_ACCESS)
    path, type_id = win32api.RegQueryValueEx(reg, 'PATH')
    path = oracle_homes[id] + ';' + path.replace(oracle_homes[id], '')
    path = path.replace(';;', ';')
    win32api.RegSetValueEx(reg, 'PATH', 0, win32con.REG_EXPAND_SZ, path)
    win32api.RegCloseKey(reg)
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')


def printHomes(oracle_homes):
    # print homes
    print '\nAvailable ORACLE_HOMEs:'
    n = 1
    for i in oracle_homes:
        print '%3d. %-15s ==> %10s' % (n, i, oracle_homes[i])
        n += 1


def interactive(oracle_homes={}):
    """ We have ORACLE_HOMEs collected. Now I'll try to change Windows
    registry and PATH system variable."""

    printHomes(oracle_homes)

    newhome = None
    while newhome == None:
        try:
            newhome = int(raw_input('Select the number of the new ORACLE_HOME (0 for quit): '))
            if len(oracle_homes) < newhome:
                newhome = None
                raise RuntimeError
        except ValueError:
            print 'I said NUMBER. Try it again.'
        except RuntimeError:
            print 'OK, nice try. Can you select one of the listed numbers?'

    if newhome == 0:
        print 'Quitting'
        sys.exit(0)

    setupHome(oracle_homes, oracle_homes.keys()[newhome - 1])


def usage():
    print \
"""
Simple ORACLE_HOME switcher for MS Windows.

usage: python %s [-h|--help] [-l|--list] [--ora=orahome]

   -h --help   prints this help
   -l --list   prints the list with available homes
   --ora=name  sets the named oracle home

The interactive mode starts when is no parameter selected.

Note that at the moment enver doesn't modify the active environment,
but only the registry so new command windows will see the changes.
So, if you type: 'set' after running enver you won't see any changes.
Setting os.environ wouldn't help because the script is executed in
a different shell then the host window.
""" % sys.argv[0]


def main():
    """ Parse arguments and call methods..."""

    o = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   'hl', ['help', 'list', 'ora='])
    except getopt.error, e:
        # print help information and exit:
        usage()
        sys.exit(2)

    for opt, value in opts:
        if opt in ('-h', '--help'):
            # print help information and exit:
            usage()
            sys.exit()
        if opt in ('-l', '--list'):
            printHomes(getAllHomes())
            sys.exit(0)
        if opt in ('--ora'):
            #print verbose messages
            o = value

    oracle_homes = getAllHomes()
    if len(oracle_homes) == 0:
        print "No oracle home found"
        sys.exit(0)

    if o == None:
        interactive(oracle_homes)
    else:
        setupHome(oracle_homes, o)

if __name__ == '__main__':
    main()

