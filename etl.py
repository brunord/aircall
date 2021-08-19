from pyspark.sql import SparkSession
from crawler.spark_processor import get_commits_all_repos_df
from crawler.spark_processor import new_montlhy_contributors
from util import data_dir
from api.api import start_api

if __name__ == "__main__":

    spark = SparkSession.builder.appName("Github Facebook Contributors ETL").getOrCreate()

    #EXTRACT/TRANSFORM
    dataset = get_commits_all_repos_df(spark).transform(new_montlhy_contributors)
    #LOAD
    dataset.coalesce(1).write.mode("Overwrite").json(data_dir)

    start_api()
