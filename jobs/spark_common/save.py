class ElasticSearch:
    def __init__(self,host_name,mode="append",write_operation="overwrite"):
        self.host_name = host_name
        self.es_mode = mode
        self.es_write_operation = write_operation
        self.es_index_auto_create = "yes"

    def write(self,df,es_resource):
        df.write \
          .mode(self.es_mode) \
          .format("org.elasticsearch.spark.sql") \
          .option("es.nodes", self.es_hots) \
          .option("es.index.auto.create", self.es_index_auto_create) \
          .option("es.resource", es_resource) \
          .save()
        