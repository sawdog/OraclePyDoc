""" Oriented graph aka ERD painter """

import types
import os
import sys
# local file subprocess24 is imported only for <2.4
if sys.version_info[:3] < (2, 4, 2):
    import subprocess24 as subprocess
else:
    import subprocess

class Dot:
    """Oriented graph aka ERD painter.

    This class requires GraphViz installed because it calls 'dot'
    externally. If it does not find that programm, no images are included
    in html docs.
    Format for parent - children: parent and [child1, child2, ..., childN]
    Format for all - {
                      parent1: [child1, child2, ..., childN],
                      parent2: [child1, child2, ..., childN],
                      ...
                      parentN: [child1, child2, ..., childN]
                     }
    """

    def __init__(self, outPath):
        ## Path to write temp files and final images
        self.outPath = outPath
        ## A flag for 'dot' availability
        self.haveDot = self.haveDot()
        ## A text template for DOT source files.
        self.graphTemplate = """
        /* This is a DOT file created by Oraschemadoc (OSD).
           When you see this file in your filesystem and OSD
           is not running, there is propably a bug in this file.
           Visit http://www.yarpen.cz/oraschemadoc and send me
           this file to fix the bug, please. */

            digraph G
            {
            label="%s";fontname="Helvetica";labelfontsize="12";
            labelloc="t";labeljust="l";labeldistance="5.0";
            edge [fontname="Helvetica",fontsize=10,labelfontname="Helvetica",labelfontsize=10];
            node [fontname="Helvetica",fontsize=10,shape=record];
            rankdir=LR;
            %s
            }
        """

    def uniq(self, aList):
        """Create a list with unique values.
        It's used for a dummy lists to be reset during diagrams source
        code creation."""
        set = {}
        map(set.__setitem__, aList, [])
        return set.keys()


    def _reSTKeyNode(self, node, highlighNode=None, anchor=None):
        """Make base node.
           Base node definiton for DOT source.

           Auto creation of the reST formatted documents generates header
           links to the foreign-keys differently then what the javadoc html
           style docs generate - so punt for now.

        """
        if anchor:
            href = "%s.html#%s" % (node, anchor)
        else:
            href = "%s.html" % node
        bgcolor = 'white'
        if highlighNode == node:
            bgcolor = 'gray88'
        s = '"%s" [label="%s" height=0.2,width=0.4,color="black",fillcolor="%s",style="filled",fontcolor="black",href="%s"];\n' % (node, node, bgcolor, href)
        return s

    def makeKeyNode(self, node, highlighNode=None):
        """Make base node.
        Base node definiton for DOT source."""
        bgcolor = 'white'
        if highlighNode == node:
            bgcolor = 'gray88'
        s = '"%s" [label="%s" height=0.2,width=0.4,color="black",fillcolor="%s",style="filled",fontcolor="black",href="table-%s.html#t-fk"];\n' % (node, node, bgcolor, node)
        return s


    def graphList(self, mainName, children=[], inverseChildren=[]):
        """Make relations between the nodes.
        Link base nodes (makeKeyNode()) together.
        \param children leafs pointing to mainName
        \param inverseChildren mainName is pointing to these leafs"""
        s = []
        for i in children:
            s.append('''"%s" -> "%s" [color="black",fontsize=10,style="solid",arrowhead="crow"];\n''' % (i, mainName))
        for i in inverseChildren:
            s.append('''"%s" -> "%s" [color="black",fontsize=10,style="solid",arrowhead="crow"];\n''' % (mainName, i))
        return ''.join(s)


    def haveDot(self):
        """! \brief Check if there is a dot installed in PATH """
        try:
            """
            if os.spawnlp(os.P_WAIT, 'dot', 'dot', '-V') == 0:
                return True
            """
            print '\nChecking for dot binary...'
            if self.runDot(['-V']) == 0:
                return True
        except OSError, e:
            print '\nUnknown error in Dot.haveDot() method. ERD disabled.'
            print '%s\n' % e
        print '    Error'
        return False

    def runDot(self, params=[]):
        """! \brief Call the 'dot' binary. Searchnig in PATH variable"""
        #return subprocess.call(["dot"] + params, env={"PATH": os.environ['PATH']}, stdout=None)
        return subprocess.call(['dot'] + params)


    def callDot(self, fname):
        """! \brief Create the PNGs and image maps from DOT files """
        f = fname + '.dot'
        retval = 1
        self.runDot(params=['-Tcmap', '-o', fname + '.map', f])
        retval = self.runDot(params=['-Tpng', '-o', fname + '.png', f])
        if retval == 0:
             try:
                 os.remove(f)
             except IOError:
                 print 'cannot delete %s' % f
        return retval

    def fileGraphList(self, mainName, children=[], inverseChildren=[],
            reST=False, anchor='referenced-by'):
        """Make a graph of the mainName's children

           XXX fugly - but seems like we need to be able to pass different
           anchor tags into the keyNode functions?
        """
        allNodes = self.uniq(children + [mainName] + inverseChildren)
        s = ''
        for i in allNodes:
            if reST:
                s += self._reSTKeyNode(i, mainName, anchor)
            else:
                s += self.makeKeyNode(i, mainName)
        s += self.graphList(mainName, children, inverseChildren)
        s = self.graphTemplate % ('ERD related to the table', s)
        fname = os.path.join(self.outPath, mainName)
        f = file(fname+'.dot', 'w')
        f.write(s)
        f.close()
        if self.callDot(fname) == 0:
            return mainName+'.png'
        return None

    def fileGraphDict(self, all={}, reST=False, name=None):
        """Make wide graph for the whole schema.

           It's used main page for the database.

           pass in name for use in sphynx when there are lots of databases,
           we need to have a unique name for each main db schema image.

        """
        if not name:
            name = 'main'

        allNodes = all.keys()
        for i in all.keys():
            if type(i) != types.ListType:
                continue
            for j in i:
                allNodes.append(j)
        allNodes = self.uniq(allNodes)
        s = ''
        for i in allNodes:
            if reST:
                s += self._reSTKeyNode(i)
            else:
                s += self.makeKeyNode(i)
        for i in all.keys():
            s += self.graphList(i, all[i])
        s = self.graphTemplate % ('ERD of the schema', s)
        fname = os.path.join(self.outPath, name)
        f = file(fname + '.dot', 'w')
        f.write(s)
        f.close()
        if self.callDot(fname) == 0:
            return '%s.png' % name

        return None


if __name__ == '__main__':
    d = Dot()
    d.fileGraphList('rodic', ['ch1', 'ch2', 'ch3'])
    d.fileGraphDict({'rodic1': ['ch1', 'ch2', 'ch3', 'rodic2'], 'rodic2': ['x1', 'rodic1']})
