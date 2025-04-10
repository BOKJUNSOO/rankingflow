import pyspark.sql.functions as F
from pyspark.sql.window import Window
from .base import Basefilter

class TableBuilder(Basefilter):
    # USER 테이블로부터 Class_Status 테이블을 만드는 함수
    def agg_class_status(self)->object:
        user_df = self.df
        filtered_df = user_df.groupBy("class","date").pivot("status") \
                      .agg(F.count("status"))
        return filtered_df
    
    # BATCH 전날과 BATCH 일의 데이터를 이용해서 AchievementSummary 테이블을 만드는 함수
    def agg_achive_summary(self)->object:
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
        
    # BATCH 전날과 BATCH 일의 joined된 데이터를 이용해서 user_exp_agg 테이블을 만드는 함수
    def agg_user_exp(self,exp_df)->object:
        joined_df = self.df
        # BATCH 전일 레벨일때 레벨업에 필요했던 경험치 컬럼을 추가
        joined_df = joined_df.join(exp_df, joined_df["character_level_yesterday"] == exp_df["level"], how='inner')
        joined_df = joined_df.select("*",F.col("need_exp").cast("long").alias("yesterday_need_exp")).drop("need_exp","level")
        # BATCH 당일 레벨일때 레벨업에 필요했던 경험치 컬럼을 추가
        joined_df = joined_df.join(exp_df, joined_df["character_level_today"] == exp_df["level"], how ='inner')
        joined_df = joined_df.select("*",F.col("need_exp").cast("long").alias("today_need_exp")).drop("need_exp","level")
        # BATCH 당일과 전일의 레벨이 동일한경우와 그렇지 않은경우를 고려한 획득한 경험치량(exp_gained_today) 계산
        joined_df = joined_df.withColumn("exp_gained_today",
                                        # 동일한 경우
                                        F.when(joined_df["character_level_today"] == joined_df["character_level_yesterday"],
                                                       (joined_df["character_exp_today"]-joined_df["character_exp_yesterday"]))
                                        # 동일하지 못한 경우
                                         .when(joined_df["character_level_yesterday"] != joined_df["character_level_yesterday"]
                                                       ,(joined_df["yesterday_need_exp"] - joined_df["character_exp_yesterday"] + joined_df["character_exp_today"])))
        # 레벨업에 필요한 경험치량(exp_remained_for_up)을 계산
        joined_df = joined_df.withColumn("exp_remained_for_up", joined_df["today_need_exp"] - joined_df["character_exp_today"])
        # 레벨업까지 필요한 예상 일자를 계산
        joined_df = joined_df.withColumn("level_up_days_remaining", F.when(joined_df["exp_gained_today"] != 0,F.round(joined_df["exp_remained_for_up"]/joined_df["exp_gained_today"]).cast("int"))
                                 .otherwise("we need you T.T"))
        
        # 지역별 경험치 획득량 계산
        rule_ = Window.partitionBy("status_today").orderBy(F.desc("exp_gained_today"))
        joined_df = joined_df.withColumn("my_rank",F.rank().over(rule_))

        # 필요한 컬럼만 선택
        user_exp_agg = joined_df.select("character_name",
                                        "date",
                                        "class",
                                    F.col("character_level_today").alias("character_level"),
                                    F.col("status_today").alias("status"),
                                        "exp_gained_today",
                                        "exp_remained_for_up",
                                        "level_up_days_remaining")
        return user_exp_agg
        
    # agg_user_exp의 리턴된 테이블로부터 class_exp_aggregate 테이블을 만드는 함수
    def agg_class_exp(self)->object:
        agg_user_exp = self.df
        class_exp_agg = agg_user_exp.groupBy("date","class","status").agg(
            F.max(agg_user_exp.exp_gained_today).alias("exp_gained_max"),
            F.sum(agg_user_exp.exp_gained_today).alias("exp_gained_sum"),
            F.round(F.mean(agg_user_exp.exp_gained_today)).cast("long").alias("exp_gained_mean")
        )
        # class별 획득 경험치의 합에따른 순위 설정
        hunt_rank = Window.partitionBy("status").orderBy(F.desc("exp_gained_sum"))
        class_exp_agg = class_exp_agg.withColumn("hunting_rank",F.rank().over(hunt_rank))
        return class_exp_agg