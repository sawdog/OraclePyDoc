"""Write out the oracle schema as xml."""

# python imports
import os

# package imports
from oraclepydoc.oraverbose import debug_message
from oraclepydoc.oraverbose import set_verbose_mode


class XMLWriter(object):
    """grab the schema and create some xml"""

    def __init__(self, cfg):
        self.cfg = cfg
        set_verbose_mode(cfg.verbose_mode)


    def write(self):
        """write out the xml files to the file system"""
        xml_file = file_name = os.path.join(self.cfg.output_dir,
                self.cfg.xml_file)
        debug_message('Creating XML file:  %s' % xml_file)
        f = open(xml_file, 'w')
        f.write(self.cfg.schema.getXML())
        f.close()
