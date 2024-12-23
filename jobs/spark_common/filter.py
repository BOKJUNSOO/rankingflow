from spark_common.base import BaseFilter
import pyspark.sql.functions as F

class DataFrameFilter():
    def agg_status(df):
        filtered_df = df.groupBy("class","date").pivot("status") \
                      .agg(F.count("status"))
        return filtered_df
    def agg_class_exp(df):
        pass
    def agg_user_exp(df):
        pass
def spark_filter():
    pass