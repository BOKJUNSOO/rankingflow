from spark_common.base import BaseFilter
import pyspark.sql.functions as F

class ClassStatusFilter(BaseFilter):
    def filter(self, df):
        filtered_df = df.groupBy("class","date").pivot("status") \
                      .agg(F.count("status"))
        return filtered_df
    

class ClassExpAggFilter(BaseFilter):
    def filter(self):
        pass

class UserExpAggFilter(BaseFilter):
    def filter(self):
        pass

def spark_filter():
    pass