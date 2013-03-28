""" List of keywords and reserverd words for Oracle SQL """

# States of the parser
WHITESPACE = 0
LINECOMMENT = 1
MULTICOMMENT = 2
KEYWORD = 3
NUMBER = 4
RESERVERD = 5
STRING = 6

operators = ['>','<','(', ')', ':', '=', '%',
             '.', ',', '/', '*', '+', '-', '!', '|']

keyWords = {
    'ALL':RESERVERD, 'ALTER':RESERVERD, 'AND':RESERVERD,
    'ANY':RESERVERD, 'ARRAY':RESERVERD, 'ARROW':RESERVERD,
    'AS':RESERVERD, 'ASC':RESERVERD, 'AT':RESERVERD,
    'BEGIN':RESERVERD, 'BETWEEN':RESERVERD, 'BY':RESERVERD,
    'CASE':RESERVERD, 'CHECK':RESERVERD, 'CLUSTERS':RESERVERD,
    'CLUSTER':RESERVERD, 'COLAUTH':RESERVERD, 'COLUMNS':RESERVERD,
    'COMPRESS':RESERVERD, 'CONNECT':RESERVERD,
    'CRASH':RESERVERD, 'CREATE':RESERVERD, 'CURRENT':RESERVERD,
    'DECIMAL':RESERVERD, 'DECLARE':RESERVERD, 'DEFAULT':RESERVERD,
    'DELETE':RESERVERD, 'DESC':RESERVERD, 'DISTINCT':RESERVERD,
    'DROP':RESERVERD, 'ELSE':RESERVERD, 'END':RESERVERD,
    'EXCEPTION':RESERVERD, 'EXCLUSIVE':RESERVERD, 'EXISTS'
    'FETCH':RESERVERD, 'FORM':RESERVERD, 'FOR':RESERVERD,
    'FROM':RESERVERD, 'GOTO':RESERVERD, 'GRANT':RESERVERD,
    'GROUP':RESERVERD, 'HAVING':RESERVERD,
    'IDENTIFIED':RESERVERD, 'IF':RESERVERD, 'IN':RESERVERD,
    'INDEXES':RESERVERD, 'INDEX':RESERVERD, 'INSERT':RESERVERD,
    'INTERSECT':RESERVERD, 'INTO':RESERVERD, 'IS':RESERVERD,
    'LIKE':RESERVERD, 'LOCK':RESERVERD,
    'MINUS':RESERVERD, 'MODE':RESERVERD,
    'NOCOMPRESS':RESERVERD, 'NOT':RESERVERD, 'NOWAIT':RESERVERD,
    'NULL':RESERVERD,
    'OF':RESERVERD, 'ON':RESERVERD, 'OPTION':RESERVERD,
    'OR':RESERVERD, 'ORDER':RESERVERD, 'OVERLAPS':RESERVERD,
    'PRIOR':RESERVERD, 'PROCEDURE':RESERVERD, 'PUBLIC':RESERVERD,
    'RANGE':RESERVERD, 'RECORD':RESERVERD, 'RESOURCE':RESERVERD,
    'REVOKE':RESERVERD,
    'SELECT':RESERVERD, 'SHARE':RESERVERD, 'SIZE':RESERVERD,
    'SQL':RESERVERD, 'START':RESERVERD, 'SUBTYPE':RESERVERD,
    'TABAUTH':RESERVERD, 'TABLE':RESERVERD, 'THEN':RESERVERD,
    'TO':RESERVERD, 'TYPE':RESERVERD,
    'UNION':RESERVERD, 'UNIQUE':RESERVERD, 'UPDATE':RESERVERD,
    'USE':RESERVERD,
    'VALUES':RESERVERD, 'VIEW':RESERVERD, 'VIEWS':RESERVERD,
    'WHEN':RESERVERD, 'WHERE':RESERVERD, 'WITH':RESERVERD,
    'A':KEYWORD, 'ADD':KEYWORD, 'AGENT':KEYWORD, 'AGGREGATE':KEYWORD,
    'ARRAY':KEYWORD, 'ATTRIBUTE':KEYWORD, 'AUTHID':KEYWORD, 'AVG':KEYWORD,
    'BFILE_BASE':KEYWORD, 'BINARY':KEYWORD, 'BLOB_BASE':KEYWORD,
    'BLOCK':KEYWORD, 'BODY':KEYWORD, 'BOTH':KEYWORD, 'BOUND':KEYWORD,
    'BULK':KEYWORD, 'BYTE':KEYWORD,
    'C':KEYWORD, 'CALL':KEYWORD, 'CALLING':KEYWORD, 'CASCADE':KEYWORD,
    'CHAR':KEYWORD, 'CHAR_BASE':KEYWORD, 'CHARACTER':KEYWORD,
    'CHARSETFORM':KEYWORD, 'CHARSETID':KEYWORD,
    'CHARSET':KEYWORD, 'CLOB_BASE':KEYWORD, 'CLOSE':KEYWORD,
    'COLLECT':KEYWORD, 'COMMENT':KEYWORD, 'COMMIT':KEYWORD,
    'COMMITTED':KEYWORD, 'COMPILED':KEYWORD,
    'CONSTANT':KEYWORD, 'CONSTRUCTOR':KEYWORD, 'CONTEXT':KEYWORD,
    'CONVERT':KEYWORD, 'COUNT':KEYWORD, 'CURSOR':KEYWORD, 'CUSTOMDATUM':KEYWORD,
    'DANGLING':KEYWORD, 'DATA':KEYWORD, 'DATE':KEYWORD,
    'DATE_BASE':KEYWORD, 'DAY':KEYWORD, 'DEFINE':KEYWORD,
    'DETERMINISTIC':KEYWORD, 'DOUBLE':KEYWORD, 'DURATION':KEYWORD,
    'ELEMENT':KEYWORD, 'ELSIF':KEYWORD, 'EMPTY':KEYWORD,
    'ESCAPE':KEYWORD, 'EXCEPT':KEYWORD, 'EXCEPTIONS':KEYWORD,
    'EXECUTE':KEYWORD, 'EXIT':KEYWORD, 'EXTERNAL':KEYWORD,
    'FINAL':KEYWORD, 'FIXED':KEYWORD, 'FLOAT':KEYWORD,
    'FORALL':KEYWORD, 'FORCE':KEYWORD, 'FUNCTION':KEYWORD,
    'GENERAL':KEYWORD,
    'HASH':KEYWORD, 'HEAP':KEYWORD, 'HIDDEN':KEYWORD, 'HOUR':KEYWORD,
    'IMMEDIATE':KEYWORD, 'INCLUDING':KEYWORD, 'INDICATOR':KEYWORD,
    'INDICES':KEYWORD, 'INFINITE':KEYWORD, 'INSTANTIABLE':KEYWORD,
    'INT':KEYWORD, 'INTERFACE':KEYWORD, 'INTERVAL':KEYWORD,
    'INVALIDATE':KEYWORD, 'ISOLATION':KEYWORD,
    'JAVA':KEYWORD,
    'LANGUAGE':KEYWORD, 'LARGE':KEYWORD, 'LEADING':KEYWORD,
    'LENGTH':KEYWORD, 'LEVEL':KEYWORD, 'LIBRARY':KEYWORD,
    'LIKE2':KEYWORD, 'LIKE4':KEYWORD, 'LIKEC':KEYWORD,
    'LIMIT':KEYWORD, 'LIMITED':KEYWORD, 'LOCAL':KEYWORD,
    'LONG':KEYWORD, 'LOOP':KEYWORD,
    'MAP':KEYWORD, 'MAX':KEYWORD, 'MAXLEN':KEYWORD,
    'MEMBER':KEYWORD, 'MERGE':KEYWORD, 'MIN':KEYWORD,
    'MINUTE':KEYWORD, 'MOD':KEYWORD, 'MODIFY':KEYWORD,
    'MONTH':KEYWORD, 'MULTISET':KEYWORD,
    'NAME':KEYWORD, 'NAN':KEYWORD, 'NATIONAL':KEYWORD,
    'NATIVE':KEYWORD, 'NCHAR':KEYWORD, 'NEW':KEYWORD,
    'NOCOPY':KEYWORD, 'NUMBER_BASE':KEYWORD,
    'OBJECT':KEYWORD, 'OCICOLL':KEYWORD, 'OCIDATETIME':KEYWORD,
    'OCIDATE':KEYWORD, 'OCIDURATION':KEYWORD, 'OCIINTERVAL':KEYWORD,
    'OCILOBLOCATOR':KEYWORD,
    'OCINUMBER':KEYWORD, 'OCIRAW':KEYWORD, 'OCIREFCURSOR':KEYWORD,
    'OCIREF':KEYWORD, 'OCIROWID':KEYWORD, 'OCISTRING':KEYWORD,
    'OCITYPE':KEYWORD, 'ONLY':KEYWORD,
    'OPAQUE':KEYWORD, 'OPEN':KEYWORD, 'OPERATOR':KEYWORD,
    'ORACLE':KEYWORD, 'ORADATA':KEYWORD, 'ORGANIZATION':KEYWORD,
    'ORLANY':KEYWORD, 'ORLVARY':KEYWORD,
    'OTHERS':KEYWORD, 'OUT':KEYWORD, 'OVERRIDING':KEYWORD,
    'PACKAGE':KEYWORD, 'PARALLEL_ENABLE':KEYWORD,
    'PARAMETER':KEYWORD, 'PARAMETERS':KEYWORD,
    'PARTITION':KEYWORD, 'PASCAL':KEYWORD, 'PIPE':KEYWORD,
    'PIPELINED':KEYWORD, 'PRAGMA':KEYWORD, 'PRECISION':KEYWORD,
    'PRIVATE':KEYWORD,
    'RAISE':KEYWORD, 'RANGE':KEYWORD, 'RAW':KEYWORD,
    'READ':KEYWORD, 'RECORD':KEYWORD, 'REF':KEYWORD,
    'REFERENCE':KEYWORD, 'REM':KEYWORD, 'REMAINDER':KEYWORD,
    'RENAME':KEYWORD, 'RESULT':KEYWORD, 'RETURN':KEYWORD,
    'RETURNING':KEYWORD, 'REVERSE':KEYWORD, 'ROLLBACK':KEYWORD,
    'ROW':KEYWORD,
    'SAMPLE':KEYWORD, 'SAVE':KEYWORD, 'SAVEPOINT':KEYWORD,
    'SB1':KEYWORD, 'SB2':KEYWORD, 'SB4':KEYWORD, 'SECOND':KEYWORD,
    'SEGMENT':KEYWORD, 'SELF':KEYWORD,
    'SEPARATE':KEYWORD, 'SEQUENCE':KEYWORD,
    'SERIALIZABLE':KEYWORD, 'SET':KEYWORD,
    'SHORT':KEYWORD, 'SIZE_T':KEYWORD, 'SOME':KEYWORD,
    'SPARSE':KEYWORD, 'SQLCODE':KEYWORD, 'SQLDATA':KEYWORD,
    'SQLNAME':KEYWORD, 'SQLSTATE':KEYWORD, 'STANDARD':KEYWORD,
    'STATIC':KEYWORD, 'STDDEV':KEYWORD, 'STORED':KEYWORD,
    'STRING':KEYWORD, 'STRUCT':KEYWORD, 'STYLE':KEYWORD,
    'SUBMULTISET':KEYWORD, 'SUBPARTITION':KEYWORD,
    'SUBSTITUTABLE':KEYWORD, 'SUBTYPE':KEYWORD,
    'SUM':KEYWORD, 'SYNONYM':KEYWORD,
    'TDO':KEYWORD, 'THE':KEYWORD, 'TIME':KEYWORD,
    'TIMESTAMP':KEYWORD, 'TIMEZONE_ABBR':KEYWORD,
    'TIMEZONE_HOUR':KEYWORD, 'TIMEZONE_MINUTE':KEYWORD,
    'TIMEZONE_REGION':KEYWORD, 'TRAILING':KEYWORD,
    'TRANSAC':KEYWORD, 'TRANSACTIONAL':KEYWORD,
    'TRUSTED':KEYWORD, 'TYPE':KEYWORD,
    'UB1':KEYWORD, 'UB2':KEYWORD, 'UB4':KEYWORD, 'UNDER':KEYWORD,
    'UNSIGNED':KEYWORD, 'UNTRUSTED':KEYWORD,
    'USE':KEYWORD, 'USING':KEYWORD,
    'VALIST':KEYWORD, 'VALUE':KEYWORD, 'VARIABLE':KEYWORD,
    'VARIANCE':KEYWORD, 'VARRAY':KEYWORD, 'VARYING':KEYWORD,
    'VOID':KEYWORD,
    'WHILE':KEYWORD, 'WORK':KEYWORD, 'WRAPPED':KEYWORD, 'WRITE':KEYWORD,
    'YEAR':KEYWORD,
    'ZONE':KEYWORD
}
