""" This module performs simple Oracle PL/SQL syntax highlighting.
It takes sql statement and produces colorized XHTML output (spanned).

The output is stored in list instead of string due Python's string
immutable behaviour - it's much more faster in the case of huge
packages e.g.
"""

import string
import re
from sqlkeywords import *


class SqlHighlighter:
    """ SQL syntax highlighter """

    def __init__(self, sql='', highlight=True):
        """ Highlighting is very slow novadays.
        Optional parameter sql is highlighted statement.
        Call parse() to start highlighting.
        Parameter highlight: True=do syntax highlighting,
                             False=without highlighting.
        """
        self.setStatement(sql)
        self.highlight = highlight


    def setStatementList(self, sql):
        """ Set statement as string from list"""
        self.sqlStatement = string.join(sql, '\n')


    def setStatement(self, sql):
        """ Provide sql statement to the class instance.
        It resets instance to the 'beginning' state too."""
        self.sqlStatement = sql
        self.status = WHITESPACE
        self.outputList = []


    def getOutput(self):
        """ Returns the result aftre parsing """
        if self.highlight:
            return ''.join(self.outputList)
        return '\n'.join(self.outputList)


    def getHeader(self, block=False):
        """ Get simple HTML legend.
        If is block set to True, it's used with <br/>"""
        if self.highlight == False:
            return 'Note: Syntax highlighting off'
            return
        if block:
            br = '<br/>'
        else:
            br = ' '
        return 'Legend:' + br \
                + '<span class="comment">comment</span>' + br \
                + '<span class="string">string</span>' + br \
                + '<span class="keyword">keyword</span>' + br \
                + '<span class="reserved">reserved word</span>' + br \
                + '<span class="operator">operator</span>'


    def parse(self, sql=None):
        """ Start parsing with given statement (parameter sql) or
        with statement previously given."""
        if sql != None:
            self.setStatement(sql)
        if self.highlight == False:
            self.outputList = self.sqlStatement.split('\n')
            return
        for i in self.sqlStatement.split('\n'):
            self._parseLine(i)
            self.outputList.append('\n')


    def _parseLine(self, line):
        """ Private method. It parses one line.
        It walks through one line/string. It takes current character,
        the it compares it for comments, strings etc. conditions - then
        it sets new state of the parser.
        Serching keywords provides regular expression for single word
        finding. It's compared with keywords and resreved words lists
        (at the top of this file)."""
        i = -1
        rowList = []
        while (i + 1) < len(line):
            i += 1
            # current character
            ch = line[i]
            # character +1
            try:
                ch1 = line[i+1]
            except:
                ch1 = ''
            # character -1
            try:
                ch2 = line[i-1]
            except:
                ch2 = ''

            # string handling 'foo'
            if self.status == WHITESPACE and ch == '\'':
                self.status = STRING
                rowList.append('<span class="string">')
                rowList.append(ch)
                continue
            if self.status == STRING and ch == '\'':
                self.status = WHITESPACE
                rowList.append(ch)
                rowList.append('</span>')
                continue
            # line comment --foo
            # rest of the line is comment
            if self.status == WHITESPACE and ch == '-' and ch1 == '-':
                rowList.append('<span class="comment">')
                rowList.append(line[i:])
                rowList.append('</span>')
                break
            # multiline comment
            if self.status == WHITESPACE and ch == '/' and ch1 == '*':
                self.status = MULTICOMMENT
                rowList.append('<span class="comment">')
                rowList.append(ch)
                continue
            if self.status == MULTICOMMENT and ch == '/' and ch2 == '*':
                self.status = WHITESPACE
                rowList.append(ch)
                rowList.append('</span>')
                continue
            # space ' ' to prevent keyword right regexp
            if self.status == WHITESPACE and ch == ' ':
                rowList.append(ch);
                continue
            # html
            if self.status == WHITESPACE and ch == '<':
                rowList.append('<span class="operator">&lt;</span>')
                continue
            if self.status == WHITESPACE and ch == '>':
                rowList.append('<span class="operator">&gt;</span>')
                continue
            # operators
            # ; removed due the speed-up
            if ch in operators and self.status == WHITESPACE:
                """if ch == '<':
                    self.outputString += '<span class="operator">&lt;</span>'
                elif ch == '>':
                    self.outputString += '<span class="operator">&gt;</span>'
                else:"""
                rowList.append('<span class="operator">')
                rowList.append(ch)
                rowList.append('</span>')
                continue
            if ch == ';' and self.status == WHITESPACE:
                rowList.append(ch)
            # aaagrh. killall tab users
            if ch == '\t' and self.status == WHITESPACE:
                rowList.append(ch)
            # keywords and reserved words
            if self.status == WHITESPACE:
                words = re.split(r'\W+', line[i:])
                current = words[0].upper()
                if len(current) == 0:
                    continue
                if keyWords.has_key(current):
                    if keyWords[current] ==  KEYWORD:
                        rowList.append('<span class="keyword">')
                        rowList.append(words[0])
                        rowList.append('</span>')
                    else:
                        rowList.append('<span class="reserved">')
                        rowList.append(words[0])
                        rowList.append('</span>')
                    i += len(current) - 1
                    continue
                rowList.append(words[0])
                i += len(words[0]) - 1
                continue
            # none condition - just put character to the output
            rowList.append(ch)
        self.outputList.append(''.join(rowList))


# unit test
if (__name__ == '__main__'):
    sql = """
FUNCTION numbers_only(
   	v_string     VARCHAR2)
 	RETURN INTEGER
 IS
   	d_length    NUMBER;
   	/*d_current	CHAR(1);
   	d_ascii  	NUMBER;
    */
 BEGIN
   --d_length := LENGTH(v_string);
   a := 8888 6666;
   FOR i IN 1 .. d_length LOOP
   	d_current := SUBSTR(v_string, i, 1);
 	IF (d_current NOT IN ('0','1','2','3','4','5','6','7','8','9')) THEN
 	  RETURN 1;
 	END IF;
    if 1 > 0 then
        null;
    end if;
   END LOOP;
   RETURN 0;
 END;
 -- simulate outer join
 select id into idno
 	from t1, t2
	where t1.col (+) = t2.col;
 """

    print """
    <html><head><title> Constraints </title>
                    <link rel="stylesheet" type="text/css" href="../oraschemadoc.css">
                    </head><body>
<pre>"""
    s = SqlHighlighter(sql, highlight=True)
    s.parse()
    print s.getHeader(block=True)
    print s.getOutput()
    print """</pre>
</body>
</html>"""

