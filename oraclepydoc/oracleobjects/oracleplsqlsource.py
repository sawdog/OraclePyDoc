class OraclePLSQLSource:
    def __init__(self, source):
        #debug_message("debug: generating plsql source ")
        self.source = []
        lines = source.keys()
        lines.sort()
        for line_no in lines:
            self.source.append(OraclePLSQLSourceLine(line_no, source[line_no]))

    def getXML(self):
        """get source in xml"""
        xml_text = '<pl_sql_source>'
        for line in self.source:
            xml_text += '<line><line_no>%s</line_no><text><![CDATA[%s]]></text></line>' % (line.line_no, line.text)
        xml_text += '</pl_sql_source>'
        return xml_text


class OraclePLSQLSourceLine:

    def __init__(self, line_no, text):
        self.line_no = line_no
        self.text = text
