import json
from functools import reduce

from pyspark.sql.functions import lit,substring,to_timestamp
from pyspark.sql.functions import min
from pyspark.sql import DataFrame
from pyspark.sql import SQLContext
from crawler.github_client import get_repos
from crawler.github_client import get_commits


def get_commits_all_repos_df(spark):
    repos = get_repos().text
    public_repositories = set(i['name'] for i in json.loads(repos))
    commits_df = list(parse_dataframe(json.loads(get_commits(repo).text), spark)
                      .withColumn("repo_name", lit(repo))
                      .select(to_timestamp("commit.author.date", "yyyy-MM-dd'T'HH:mm:ss'Z'").alias("date"), "commit.author.email", "repo_name")
                      for repo in public_repositories)

    return union_all(*commits_df)


def new_montlhy_contributors(df: DataFrame):
    new_df = df.groupBy("email", "repo_name").agg(min("date").alias("first_commit")) \
        .withColumn("month", substring("first_commit", 1,7)) \
        .groupBy("repo_name", "month").count().alias("number_of_new_contributors")
    return new_df


def union_all(*dfs):
    return reduce(DataFrame.union, dfs)


def convert_single_object_per_line(json_list):
    json_string = ""
    for line in json_list:
        json_string += json.dumps(line) + "\n"
    return json_string


def parse_dataframe(json_data, spark):
    r = convert_single_object_per_line(json_data)
    mylist = []
    for line in r.splitlines():
        mylist.append(line)
    rdd = spark.sparkContext.parallelize(mylist)
    df = SQLContext(spark.sparkContext).read.json(rdd)
    return df