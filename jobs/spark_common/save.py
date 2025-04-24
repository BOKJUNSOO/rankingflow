class ElasticSearch:
    def __init__(self,host_name,es_port="9200",es_nodes_discovery ="false",es_nodes_wan="true",es_index_auto_create="true"):
        self.host_name = host_name
        self.es_port = es_port
        self.es_nodes_discovery = es_nodes_discovery
        self.es_nodes_wan = es_nodes_wan
        self.es_index_auto_create = es_index_auto_create
        
    def write(self,df,es_resource):
        df.write \
          .mode("append") \
          .format("org.elasticsearch.spark.sql") \
          .option("es.nodes",self.host_name) \
          .option("es.port", self.es_port) \
          .option("es.nodes.discovery", self.es_nodes_discovery)\
          .option("es.nodes.wan.only", self.es_nodes_wan)\
          .option("es.index.auto.create", self.es_index_auto_create) \
          .option("es.resource", es_resource) \
          .save()

class MySQL:
    def __init__(self,url:str,user="root",password="password"):
        self.url = url
        self.user = user
        self.password = password
    
    def write(self,df:object,db_table_name:str):
        df.write \
          .mode("overwrite")\
          .format("jdbc")\
          .option("driver","com.mysql.cj.jdbc.Driver")\
          .option("url",self.url)\
          .option("user",self.user)\
          .option("password",self.password)\
          .option("dbtable",db_table_name)\
          .save()
        
