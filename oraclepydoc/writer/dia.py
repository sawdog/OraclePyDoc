"""Dia diagram writer"""

# python imports
import os

# package imports
from oraschemadoc.formatter.dia import DiaUmlDiagramGenerator
from oraschemadoc.oraverbose import debug_message
from oraschemadoc.oraverbose import set_verbose_mode

class DiaWriter(object):
    """write out the dia diagram."""

    def __init__(self, cfg):
        self.cfg = cfg
        set_verbose_mode(cfg.verbose_mode)

    def write(self):
        dia_file = os.path.join(self.cfg.output_dir,
                self.cfg.dia_file_name)

        debug_message('Creating DIA file: %s' % dia_file)
        DiaUmlDiagramGenerator(self.cfg.schema, dia_file, self.cfg.desc,
                0, self.cfg.dia_conf_file)
