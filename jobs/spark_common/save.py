class ElasticSearch:
    def __init__(self,host_name,port = 9200,es_nodes_wan = True,es_mode="append",write_operation="overwrite"):
        self.host_name = host_name
        self.es_mode = es_mode
        self.es_write_operation = write_operation
        self.es_index_auto_create = "yes"
        self.port = port
        self.es_nodes_wan = es_nodes_wan


    def write(self,df,es_resource):
        df.write \
          .mode(self.es_mode) \
          .format("org.elasticsearch.spark.sql") \
          .option("es.nodes.wan.only", self.es_nodes_wan)\
          .option("es.port", self.port) \
          .option("es.nodes", self.host_name) \
          .option("es.index.auto.create", self.es_index_auto_create) \
          .option("es.resource", es_resource) \
          .save()
        