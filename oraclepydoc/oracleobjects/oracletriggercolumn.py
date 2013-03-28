class OracleTriggerColumn:

    def __init__(self, column_name, column_list, column_usage):
        #debug_message("debug: generating trigger column %s" % column_name)
        self.column_name = column_name
        self.column_list = column_list
        self.column_usage = column_usage
