from oracleview import OracleView


class OracleMView(OracleView):

    def __init__(self, name, data_dict):
        # FIXME: real inheritance! OracleView.__init__(self, name, data_dict)
        self.name = name
        self.columns = self._get_columns(data_dict)
        self.constraints = self._get_constraints(data_dict)
        self.comments = data_dict.all_table_comments.get(name)
        self.triggers = self._get_triggers(data_dict)
        self.container, self.query, self.mv_updatable = data_dict.all_mviews[name]
        self.text = self.query
