class OracleJob:
    """! \brief Represents Oracle job"""

    def __init__(self, job, log_user, priv_user, schema_user,
                 total_time, broken, interval, failures, what):
        self.job = job
        self.log_user = log_user
        self.priv_user = priv_user
        self.schema_user = schema_user
        self.total_time = str(total_time)
        self.broken = broken
        self.interval = interval
        self.failures = str(failures)
        self.what = what


    def getXML(self):
        """get job's metadata in xml"""
        xml_text = '''<job id="job-%s">
                        <job>%s</job>
                        <log_user>%s</log_user>
                        <priv_user>%s</priv_user>
                        <schema_user>%s</schema_user>
                        <total_time>%s</total_time>
                        <broken>%s</broken>
                        <interval>%s</interval>
                        <failures>%s</failures>
                        <what>%s</what>
                      </sequence>''' % (self.job, self.job, self.log_user, self.priv_user,
                                        self.schema_user, self.total_time, self.broken,
                                        self.interval, self.failures, self.what)
        return xml_text

