class OracleTabPartition:

    def __init__(self, partition_position, partition_name, tablespace_name, high_value):
        self.partition_position = partition_position
        self.partition_name = partition_name
        self.tablespace_name = tablespace_name
        self.high_value = high_value
