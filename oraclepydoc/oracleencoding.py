#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

""" Helper class for Oracle/Python charsets and encoding manipulation """
class OracleNLSCharset:

    def __init__(self):
        """ Basic operations with Python/Oracle character sets.
        We are so lazy to write all stuff here (ora2py, py2ora)
        so you should fix it yourself. Send it to us then, please."""

        # Oracle NLS -> (Python codec name, web encoding string) mapping
        self._ora2py = {
            #'AL16UTF16':''
            #'AL24UTFFSS':''
            'AL32UTF8': ('utf-8', 'utf-8'),
            #'AR8ADOS710':''
            #'AR8ADOS710T':''
            #'AR8ADOS720':''
            #'AR8ADOS720T':''
            #'AR8APTEC715':''
            #'AR8APTEC715T':''
            #'AR8ARABICMAC':''
            #'AR8ARABICMACS':''
            #'AR8ARABICMACT':''
            #'AR8ASMO708PLUS':''
            #'AR8ASMO8X':''
            #'AR8EBCDICX':''
            #'AR8EBCDIC420S':''
            #'AR8HPARABIC8T':''
            'AR8ISO8859P6': ('iso-8859-6', 'iso-8859-6'),
            #'AR8MSAWIN':''
            'AR8MSWIN1256': ('cp1250', 'windows-1256'),
            #'AR8MUSSAD768':''
            #'AR8MUSSAD768T':''
            #'AR8NAFITHA711':''
            #'AR8NAFITHA711T':''
            #'AR8NAFITHA721':''
            #'AR8NAFITHA721T':''
            #'AR8SAKHR706':''
            #'AR8SAKHR707':''
            #'AR8SAKHR707T':''
            #'AR8XBASIC':''
            #'BG8MSWIN':''
            #'BG8PC437S':''
            #'BLT8CP921':''
            #'BLT8EBCDIC1112':''
            #'BLT8EBCDIC1112S':''
            'BLT8ISO8859P13':('iso-8859-13', 'iso-8859-13'),
            'BLT8MSWIN1257':('cp1250', 'windows-1257'),
            'BLT8PC775': ('cp775', 'cp775'),
            #'BN8BSCII':''
            'CDN8PC863': ('cp863', 'cp863'),
            'CEL8ISO8859P14': ('iso-8859-14', 'iso-8859-14'),
            #'CE8BS2000':''
            #'CH7DEC':''
            #'CL8BS2000':''
            #'CL8EBCDIC1025':''
            #'CL8EBCDIC1025C':''
            #'CL8EBCDIC1025R':''
            #'CL8EBCDIC1025S':''
            #'CL8EBCDIC1025X':''
            #'CL8EBCDIC1158':''
            #'CL8EBCDIC1158R':''
            #'CL8ISOIR111':''
            'CL8ISO8859P5': ('iso-8859-5', 'iso-8859-5'),
            'CL8KOI8R': ('koi8-r', 'koi8-r'),
            'CL8KOI8U': ('koi8-u', 'koi8-u'),
            'CL8MACCYRILLIC': ('x-mac-cyrillic', 'x-mac-cyrillic'),
            #'CL8MACCYRILLICS':''
            'CL8MSWIN1251': ('cp1251', 'windows-1251'),
            #'DK7SIEMENS9780X':''
            #'DK8BS2000':''
            #'DK8EBCDIC1142':''
            #'DK8EBCDIC277':''
            #'D7DEC':''
            #'D7SIEMENS9780X':''
            #'D8BS2000':''
            #'D8EBCDIC1141':''
            #'D8EBCDIC273':''
            #'EEC8EUROASCI':''
            #'EEC8EUROPA3':''
            #'EE8BS2000':''
            #'EE8EBCDIC870':''
            #'EE8EBCDIC870C':''
            #'EE8EBCDIC870S':''
            'EE8ISO8859P2': ('iso-8859-2', 'iso-8859-2'),
            #'EE8MACCE':''
            #'EE8MACCES':''
            #'EE8MACCROATIAN':''
            #'EE8MACCROATIANS':''
            'EE8MSWIN1250': ('cp1250', 'windows-1250'),
            'EE8PC852': ('cp852', 'cp852'),
            #'EL8DEC':''
            #'EL8EBCDIC423R':''
            #'EL8EBCDIC875':''
            #'EL8EBCDIC875R':''
            #'EL8EBCDIC875S':''
            #'EL8GCOS7':''
            'EL8ISO8859P7': ('iso-8859-7', 'iso-8859-7'),
            'EL8MACGREEK': ('x-mac-greek', 'x-mac-greek'),
            #'EL8MACGREEKS':''
            'EL8MSWIN1253': ('cp1253', 'windows-1253'),
            #'EL8PC437S':''
            'EL8PC737': ('cp737', 'cp737'),
            'EL8PC851': ('cp851', 'cp851'),
            'EL8PC869': ('cp869', 'cp869'),
            'ET8MSWIN923': ('cp923', 'windows-923'),
            #'E7DEC':''
            #'E7SIEMENS9780X':''
            #'E8BS2000':''
            #'F7DEC':''
            #'F7SIEMENS9780X':''
            #'F8BS2000':''
            #'F8EBCDIC1147':''
            #'F8EBCDIC297':''
            #'HU8ABMOD':''
            #'HU8CWI2':''
            #'HZ-GB-2312':''
            #'IN8ISCII':''
            #'ISO2022-CN':''
            #'ISO2022-JP':''
            #'ISO2022-KR':''
            #'IS8MACICELANDIC':''
            #'IS8MACICELANDICS':''
            'IS8PC861': ('cp861', 'cp861'),
            #'IW7IS960':''
            #'IW8EBCDIC1086':''
            #'IW8EBCDIC424':''
            #'IW8EBCDIC424S':''
            'IW8ISO8859P8': ('iso-8859-8', 'iso-8859-8'),
            #'IW8MACHEBREW':''
            #'IW8MACHEBREWS':''
            'IW8MSWIN1255': ('cp1255', 'windows-1255'),
            'IW8PC1507': ('cp1507', 'cp1507'),
            #'I7DEC':''
            #'I7SIEMENS9780X':''
            #'I8EBCDIC1144':''
            #'I8EBCDIC280':''
            #'JA16DBCS':''
            #'JA16DBCSFIXED':''
            #'JA16EBCDIC930':''
            #'JA16EUC':''
            #'JA16EUCFIXED':''
            #'JA16EUCTILDE':''
            #'JA16EUCYEN':''
            #'JA16MACSJIS':''
            'JA16SJIS': ('Shift_JIS', 'Shift_JIS'),
            #'JA16SJISFIXED':''
            #'JA16SJISTILDE':''
            #'JA16SJISYEN':''
            #'JA16TSTSET':''
            #'JA16TSTSET2':''
            #'JA16VMS':''
            #'KO16DBCS':''
            #'KO16DBCSFIXED':''
            #'KO16KSCCS':''
            #'KO16KSC5601':''
            #'KO16KSC5601FIXED':''
            'KO16MSWIN949': ('cp949', 'windows-949'),
            #'KO16TSTSET':''
            #'LA8ISO6937':''
            #'LA8PASSPORT':''
            'LT8MSWIN921': ('cp921', 'windows-921'),
            'LT8PC772': ('cp772', 'cp772'),
            'LT8PC774': ('cp774', 'cp774'),
            'LV8PC1117': ('cp1117', 'cp1117'),
            #'LV8PC8LR':''
            #'LV8RST104090':''
            #'NDK7DEC':''
            'NEE8ISO8859P4': ('iso-8859-4', 'iso-8859-4'),
            'NE8ISO8859P10': ('iso-8859-10', 'iso-8859-10'),
            #'NL7DEC':''
            #'N7SIEMENS9780X':''
            'N8PC865': ('cp865', 'cp865'),
            #'RU8BESTA':''
            'RU8PC855': ('cp855', 'cp865'),
            'RU8PC866': ('cp866', 'cp866'),
            'SE8ISO8859P3': ('iso-8859-3', 'iso-8859-3'),
            #'SF7ASCII':''
            #'SF7DEC':''
            #'S7DEC':''
            #'S7SIEMENS9780X':''
            #'S8BS2000':''
            #'S8EBCDIC1143':''
            #'S8EBCDIC278':''
            #'TH8MACTHAI':''
            #'TH8MACTHAIS':''
            #'TH8TISASCII':''
            #'TH8TISEBCDIC':''
            #'TH8TISEBCDICS':''
            #'TR7DEC':''
            #'TR8DEC':''
            #'TR8EBCDIC1026':''
            #'TR8EBCDIC1026S':''
            #'TR8MACTURKISH':''
            #'TR8MACTURKISHS':''
            'TR8MSWIN1254': ('cp1254', 'windows-1254'),
            'TR8PC857':'cp857',
            #'US16TSTFIXED':''
            #'US7ASCII':'us_ascii',
            'US7ASCII': 'utf-8',
            #'US8BS2000':''
            #'US8ICL':''
            'US8PC437':'cp437',
            #'UTFE':''
            'UTF8': ('utf-8', 'utf-8'),
            'VN8MSWIN1258': ('cp1258', 'windows-1258'),
            #'VN8VN3':''
            #'WE16DECTST':''
            #'WE16DECTST2':''
            #'WE8BS2000':''
            #'WE8BS2000E':''
            #'WE8BS2000L5':''
            #'WE8DEC':''
            #'WE8DECTST':''
            #'WE8DG':''
            #'WE8EBCDIC1047':''
            #'WE8EBCDIC1047E':''
            #'WE8EBCDIC1140':''
            #'WE8EBCDIC1140C':''
            #'WE8EBCDIC1145':''
            #'WE8EBCDIC1146':''
            #'WE8EBCDIC1148':''
            #'WE8EBCDIC1148C':''
            #'WE8EBCDIC284':''
            #'WE8EBCDIC285':''
            #'WE8EBCDIC37':''
            #'WE8EBCDIC37C':''
            #'WE8EBCDIC500':''
            #'WE8EBCDIC500C':''
            #'WE8EBCDIC871':''
            #'WE8EBCDIC924':''
            #'WE8GCOS7':''
            #'WE8HP':''
            #'WE8ICL':''
            #'WE8ISOICLUK':''
            'WE8ISO8859P1': ('iso-8859-1', 'iso-8859-1'),
            'WE8ISO8859P15': ('iso-8859-15', 'iso-8859-15'),
            'WE8ISO8859P9': ('iso-8859-9', 'iso-8859-9'),
            #'WE8MACROMAN8':''
            #'WE8MACROMAN8S':''
            'WE8MSWIN1252': ('cp1252', 'windows-1252'),
            #'WE8NCR4970':''
            #'WE8NEXTSTEP':''
            'WE8PC850': ('cp850', 'cp850'),
            'WE8PC858': ('cp858', 'cp858'),
            'WE8PC860': ('cp860', 'cp860'),
            #'WE8ROMAN8':''
            #'YUG7ASCII':''
            #'ZHS16CGB231280':''
            #'ZHS16CGB231280FIXED':''
            #'ZHS16DBCS':''
            #'ZHS16DBCSFIXED':''
            #'ZHS16GBK':''
            #'ZHS16GBKFIXED':''
            #'ZHS16MACCGB231280':''
            #'ZHS32GB18030':''
            #'ZHT16BIG5':''
            #'ZHT16BIG5FIXED':''
            #'ZHT16CCDC':''
            #'ZHT16DBCS':''
            #'ZHT16DBCSFIXED':''
            #'ZHT16DBT':''
            #'ZHT16HKSCS':''
            'ZHT16MSWIN950': ('cp950', 'windows-950')
            #'ZHT32EUC':''
            #'ZHT32EUCFIXED':''
            #'ZHT32EUCTST':''
            #'ZHT32SOPS':''
            #'ZHT32TRIS':''
            #'ZHT32TRISFIXED':''
        }

        # Python codec name -> Oracle NLS mapping
        self._py2ora = {
            #'':'AL16UTF16'
            #'':'AL24UTFFSS'
            #'':'AL32UTF8'
            #'':'AR8ADOS710'
            #'':'AR8ADOS710T'
            #'':'AR8ADOS720'
            #'':'AR8ADOS720T'
            #'':'AR8APTEC715'
            #'':'AR8APTEC715T'
            #'':'AR8ARABICMAC'
            #'':'AR8ARABICMACS'
            #'':'AR8ARABICMACT'
            #'':'AR8ASMO708PLUS'
            #'':'AR8ASMO8X'
            #'':'AR8EBCDICX'
            #'':'AR8EBCDIC420S'
            #'':'AR8HPARABIC8T'
            'iso8859-6':'AR8ISO8859P6',
            #'':'AR8MSAWIN'
            'windows-1256':'AR8MSWIN1256',
            #'':'AR8MUSSAD768'
            #'':'AR8MUSSAD768T'
            #'':'AR8NAFITHA711'
            #'':'AR8NAFITHA711T'
            #'':'AR8NAFITHA721'
            #'':'AR8NAFITHA721T'
            #'':'AR8SAKHR706'
            #'':'AR8SAKHR707'
            #'':'AR8SAKHR707T'
            #'':'AR8XBASIC'
            #'':'BG8MSWIN'
            #'':'BG8PC437S'
            'cp921':'BLT8CP921',
            #'':'BLT8EBCDIC1112'
            #'':'BLT8EBCDIC1112S'
            'iso-8859-13':'BLT8ISO8859P13',
            'windows-1257':'BLT8MSWIN1257',
            'cp775':'BLT8PC775',
            #'':'BN8BSCII'
            'cp863':'CDN8PC863',
            'iso-8859-14':'CEL8ISO8859P14',
            #'':'CE8BS2000'
            #'':'CH7DEC'
            #'':'CL8BS2000'
            #'':'CL8EBCDIC1025'
            #'':'CL8EBCDIC1025C'
            #'':'CL8EBCDIC1025R'
            #'':'CL8EBCDIC1025S'
            #'':'CL8EBCDIC1025X'
            #'':'CL8EBCDIC1158'
            #'':'CL8EBCDIC1158R'
            #'':'CL8ISOIR111'
            'iso-8859-5':'CL8ISO8859P5',
            'koi8-r':'CL8KOI8R',
            'koi8-u':'CL8KOI8U',
            'x-mac-cyrillic':'CL8MACCYRILLIC',
            #'':'CL8MACCYRILLICS'
            'windows-1251':'CL8MSWIN1251',
            #'':'DK7SIEMENS9780X'
            #'':'DK8BS2000'
            #'':'DK8EBCDIC1142'
            #'':'DK8EBCDIC277'
            #'':'D7DEC'
            #'':'D7SIEMENS9780X'
            #'':'D8BS2000'
            #'':'D8EBCDIC1141'
            #'':'D8EBCDIC273'
            #'':'EEC8EUROASCI'
            #'':'EEC8EUROPA3'
            #'':'EE8BS2000'
            #'':'EE8EBCDIC870'
            #'':'EE8EBCDIC870C'
            #'':'EE8EBCDIC870S'
            'iso-8859-2':'EE8ISO8859P2',
            #'':'EE8MACCE'
            #'':'EE8MACCES'
            #'':'EE8MACCROATIAN'
            #'':'EE8MACCROATIANS'
            'cp1250':'EE8MSWIN1250',
            'cp852':'EE8PC852',
            #'':'EL8DEC'
            #'':'EL8EBCDIC423R'
            #'':'EL8EBCDIC875'
            #'':'EL8EBCDIC875R'
            #'':'EL8EBCDIC875S'
            #'':'EL8GCOS7'
            'iso-8859-7':'EL8ISO8859P7',
            'x-mac-greek':'EL8MACGREEK',
            #'':'EL8MACGREEKS'
            'windows-1253':'EL8MSWIN1253',
            #'':'EL8PC437S'
            'cp737':'EL8PC737',
            'cp851':'EL8PC851',
            'cp869':'EL8PC869',
            'windows-923':'ET8MSWIN923',
            #'':'E7DEC'
            #'':'E7SIEMENS9780X'
            #'':'E8BS2000'
            #'':'F7DEC'
            #'':'F7SIEMENS9780X'
            #'':'F8BS2000'
            #'':'F8EBCDIC1147'
            #'':'F8EBCDIC297'
            #'':'HU8ABMOD'
            #'':'HU8CWI2'
            #'':'HZ-GB-2312'
            #'':'IN8ISCII'
            #'':'ISO2022-CN'
            #'':'ISO2022-JP'
            #'':'ISO2022-KR'
            #'':'IS8MACICELANDIC'
            #'':'IS8MACICELANDICS'
            'cp861':'IS8PC861',
            'cp960':'IW7IS960',
            #'':'IW8EBCDIC1086'
            #'':'IW8EBCDIC424'
            #'':'IW8EBCDIC424S'
            'iso-8859-8':'IW8ISO8859P8',
            #'':'IW8MACHEBREW'
            #'':'IW8MACHEBREWS'
            'windows-1255':'IW8MSWIN1255',
            'cp1507':'IW8PC1507',
            #'':'I7DEC'
            #'':'I7SIEMENS9780X'
            #'':'I8EBCDIC1144'
            #'':'I8EBCDIC280'
            #'':'JA16DBCS'
            #'':'JA16DBCSFIXED'
            #'':'JA16EBCDIC930'
            #'':'JA16EUC'
            #'':'JA16EUCFIXED'
            #'':'JA16EUCTILDE'
            #'':'JA16EUCYEN'
            #'':'JA16MACSJIS'
            #'':'JA16SJIS'
            #'':'JA16SJISFIXED'
            #'':'JA16SJISTILDE'
            #'':'JA16SJISYEN'
            #'':'JA16TSTSET'
            #'':'JA16TSTSET2'
            #'':'JA16VMS'
            #'':'KO16DBCS'
            #'':'KO16DBCSFIXED'
            #'':'KO16KSCCS'
            #'':'KO16KSC5601'
            #'':'KO16KSC5601FIXED'
            'windows-949':'KO16MSWIN949',
            #'':'KO16TSTSET'
            'iso-6937':'LA8ISO6937',
            #'':'LA8PASSPORT'
            'windows-921':'LT8MSWIN921',
            'cp772':'LT8PC772',
            'cp774':'LT8PC774',
            'cp1117':'LV8PC1117',
            #'':'LV8PC8LR'
            #'':'LV8RST104090'
            #'':'NDK7DEC'
            'iso-8859-4':'NEE8ISO8859P4',
            'iso-8859-10':'NE8ISO8859P10',
            #'':'NL7DEC'
            #'':'N7SIEMENS9780X'
            'cp865':'N8PC865',
            #'':'RU8BESTA'
            'cp855':'RU8PC855',
            'cp866':'RU8PC866',
            'iso-8859-3':'SE8ISO8859P3',
            #'':'SF7ASCII'
            #'':'SF7DEC'
            #'':'S7DEC'
            #'':'S7SIEMENS9780X'
            #'':'S8BS2000'
            #'':'S8EBCDIC1143'
            #'':'S8EBCDIC278'
            #'':'TH8MACTHAI'
            #'':'TH8MACTHAIS'
            #'':'TH8TISASCII'
            #'':'TH8TISEBCDIC'
            #'':'TH8TISEBCDICS'
            #'':'TR7DEC'
            #'':'TR8DEC'
            #'':'TR8EBCDIC1026'
            #'':'TR8EBCDIC1026S'
            #'':'TR8MACTURKISH'
            #'':'TR8MACTURKISHS'
            'windows-1254':'TR8MSWIN1254',
            'cp857':'TR8PC857',
            #'':'US16TSTFIXED'
            'us_ascii':'US7ASCII',
            #'':'US8BS2000'
            #'':'US8ICL'
            'cp437':'US8PC437',
            #'':'UTFE'
            'utf-8':'UTF8',
            'windows-1258':'VN8MSWIN1258',
            #'':'VN8VN3'
            #'':'WE16DECTST'
            #'':'WE16DECTST2'
            #'':'WE8BS2000'
            #'':'WE8BS2000E'
            #'':'WE8BS2000L5'
            #'':'WE8DEC'
            #'':'WE8DECTST'
            #'':'WE8DG'
            #'':'WE8EBCDIC1047'
            #'':'WE8EBCDIC1047E'
            #'':'WE8EBCDIC1140'
            #'':'WE8EBCDIC1140C'
            #'':'WE8EBCDIC1145'
            #'':'WE8EBCDIC1146'
            #'':'WE8EBCDIC1148'
            #'':'WE8EBCDIC1148C'
            #'':'WE8EBCDIC284'
            #'':'WE8EBCDIC285'
            #'':'WE8EBCDIC37'
            #'':'WE8EBCDIC37C'
            #'':'WE8EBCDIC500'
            #'':'WE8EBCDIC500C'
            #'':'WE8EBCDIC871'
            #'':'WE8EBCDIC924'
            #'':'WE8GCOS7'
            #'':'WE8HP'
            #'':'WE8ICL'
            #'':'WE8ISOICLUK'
            'iso-8859-1':'WE8ISO8859P1',
            'iso-8859-15':'WE8ISO8859P15',
            'iso-8859-9':'WE8ISO8859P9',
            #'':'WE8MACROMAN8'
            #'':'WE8MACROMAN8S'
            'windows-1252':'WE8MSWIN1252',
            #'':'WE8NCR4970'
            #'':'WE8NEXTSTEP'
            'cp850':'WE8PC850',
            'cp858':'WE8PC858',
            'cp860':'WE8PC860',
            #'':'WE8ROMAN8'
            #'':'YUG7ASCII'
            #'':'ZHS16CGB231280'
            #'':'ZHS16CGB231280FIXED'
            #'':'ZHS16DBCS'
            #'':'ZHS16DBCSFIXED'
            #'':'ZHS16GBK'
            #'':'ZHS16GBKFIXED'
            #'':'ZHS16MACCGB231280'
            #'':'ZHS32GB18030'
            #'':'ZHT16BIG5'
            #'':'ZHT16BIG5FIXED'
            #'':'ZHT16CCDC'
            #'':'ZHT16DBCS'
            #'':'ZHT16DBCSFIXED'
            #'':'ZHT16DBT'
            #'':'ZHT16HKSCS'
            'windows-950':'ZHT16MSWIN950'
            #'':'ZHT32EUC'
            #'':'ZHT32EUCFIXED'
            #'':'ZHT32EUCTST'
            #'':'ZHT32SOPS'
            #'':'ZHT32TRIS'
            #'':'ZHT32TRISFIXED'
        }

    def getClientNLSCharset(self):
        """ Try to know default client encoding.
        Env vars have bigger priority than registers. """
        try:
            env = os.environ['NLS_LANG']
            return env.split('.')[1]
        except KeyError:
            print 'NLS_LANG: environment var not found.'
        try:
            return os.environ['NLS_CHARSET']
        except KeyError:
            print 'NLS_CHARSET: environment var not found.'
        # TODO: _winreg here!
        return None

    def getOracleNLSCharacterset(self, cx_connection):
        """ Returns charset name of the connected database.
        V$NLS_PARAMETERS is publis synonym with SELECT grant to public
        so don't be afraid of insuff. privs. exceptions."""
        cursor = cx_connection.cursor()
        cursor.execute('SELECT value FROM v$nls_parameters WHERE parameter=\'NLS_CHARACTERSET\'')
        oraCharset = cursor.fetchone()[0]
        cursor.close()
        return oraCharset

    def getOracleEncoding(self, pythonCodec):
        """ Returns Oracle language value for given Python codec name """
        try:
            return self._py2ora[pythonCodec]
        except KeyError:
            print 'Oracle NLS_CHARSET value for codec %s not found.' % pythonCodec
            self.warning()

    def getPythonEncoding(self, oracleNLSCharset):
        """ Returns Python codec valid for Oracle language name """
        try:
            return self._ora2py[oracleNLSCharset]
        except KeyError:
            print 'Python codec for Oracle NLS_CHARSET %s not found.' % oracleNLSCharset
            self.warning()

    def warning(self):
        """ Write some info in the case of the missing encoding """
        print '''
    It's propably my fault, 'cos I'm too lazy to fill
    all available combinations. Obtain the source file
    oracleencoding.py and fix it. Or send me a email
    with your values.
'''


if __name__ == '__main__':
    # only chickens use unit tests...
    import cx_Oracle
    #connection = cx_Oracle.connect('s0/s0@s0test')
    ora = OracleNLSCharset()
    #print ora.getOracleNLSCharacterset(connection)
    #connection.close()
    print ora.getClientNLSCharset()
    print ora.getPythonEncoding('UTF8')
    print ora.getOracleEncoding('ISO-8859-2')
    print ora.getOracleEncoding('iso8859_2')
    print ora.getOracleEncoding('iso-8859-2')
