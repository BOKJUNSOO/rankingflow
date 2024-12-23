import pyspark.sql.functions as F

class StatusFilter:
    def __init__(self,df):
        self.df = df
    # USER 테이블로부터 Class_Status 테이블을 만드는 함수
    def agg_class_status(self):
        df = self.df
        filtered_df = df.groupBy("class","date").pivot("status") \
                      .agg(F.count("status"))
        return filtered_df
    
    # BATCH 전날과 BATCH 일의 데이터를 이용해서 AchievementSummary 테이블을 만드는 함수
    def agg_achive_summary(self):
        joined_df = self.df
        achive_df=joined_df.select("class","date","status_today","status_yesterday")
        achive_df=achive_df.withColumn("status_change", F.when((achive_df["status_today"] == achive_df["status_yesterday"]) , "stayhere" )
                                                    .when((achive_df["status_today"] != achive_df["status_yesterday"])&(achive_df["status_today"]=="Tallahart"), "welcome to Tallahart")
                                                    .when((achive_df["status_today"] != achive_df["status_yesterday"])&(achive_df["status_today"]=="Carcion"), "welcome to Carcion")
                                                    .when((achive_df["status_today"] != achive_df["status_yesterday"])&(achive_df["status_today"]=="Arteria"), "welcome to Arteria")
                                                    .when((achive_df["status_today"] != achive_df["status_yesterday"])&(achive_df["status_today"]=="Dowonkyung"), "welcome to Dowonkyung")
                                                    .when((achive_df["status_today"] != achive_df["status_yesterday"])&(achive_df["status_today"]=="Odium"), "welcome to Odium")
                                                    .when((achive_df["status_today"] != achive_df["status_yesterday"])&(achive_df["status_today"]=="HotelArcs"), "welcome to HotelArcs")
                                                    .when((achive_df["status_today"] != achive_df["status_yesterday"])&(achive_df["status_today"]=="Cernium"), "welcome to Cernium"))
        achive_df = achive_df.groupBy("class","date","status_change").agg(F.count("*").alias("count"))
        return achive_df

class ExpFilter:
    def __init__(self,df,exp_df):
        self.df = df
        self.exp_df = df
    # BATCH 전날과 BATCH 일의 데이터를 이용해서 user_exp_aggregate 테이블을 만드는 함수
    def agg_user_exp(self):
        joined_df = self.df
        exp_df = self.exp_df
        
    # agg_user_exp의 리턴된 테이블로부터 class_exp_aggregate 테이블을 만드는 함수
    def agg_class_exp(self,df):
        pass
    
    

def spark_filter():
    pass