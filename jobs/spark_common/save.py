class ElasticSearch:
    def __init__(self,host_name,es_nodes_discovery ="false",es_nodes_wan="true",es_index_auto_create="true",es_mapping_id = "id",es_mapping_exclude="id"):
        self.host_name = host_name
        self.es_nodes_discovery = es_nodes_discovery
        self.es_nodes_wan = es_nodes_wan
        self.es_index_auto_create = es_index_auto_create
        self.es_mapping_id = es_mapping_id
        self.es_mapping_exclude = es_mapping_exclude
        


    def write(self,df,es_resource):
        df.write \
          .format("org.elasticsearch.spark.sql") \
          .option("es.nodes",self.host_name) \
          .option("es.nodes.discovery", self.es_nodes_discovery)\
          .option("es.nodes.wan.only", self.es_nodes_wan)\
          .option("es.index.auto.create", self.es_index_auto_create) \
          .option("es.mapping.id",self.es_mapping_id)\
          .option("es.mapping.exclude",self.es_mapping_exclude) \
          .option("es.resource", es_resource) \
          .save()
        