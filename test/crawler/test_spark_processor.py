from pyspark.sql import SparkSession
import unittest
from crawler.spark_processor import new_montlhy_contributors


class TestSparkProcessor(unittest.TestCase):

    def test_new_montlhy_contributors(self):

        spark = SparkSession.builder.appName('test').getOrCreate()

        commits = [("a","repo_1", "2021-01-31T12:00:00Z"),
                   ("a","repo_1", "2021-02-31T12:00:00Z"),
                   ("a","repo_1", "2021-03-31T12:00:00Z"),
                   ("a","repo_2", "2021-02-31T12:00:00Z"),

                   ("b","repo_2", "2021-02-31T12:00:00Z"),
                   ("b","repo_3", "2021-03-31T12:00:00Z"),

                   ("d","repo_3", "2021-03-31T12:00:00Z"),
                   ("d","repo_3", "2021-04-31T12:00:00Z"),

                   ("e","repo_3", "2021-04-31T12:00:00Z")
        ]

        commits_columns = ["email","repo_name", "date"]
        df_before = spark.createDataFrame(data=commits, schema = commits_columns)

        df_after = df_before.transform(new_montlhy_contributors)
        new_contributors = [("repo_3","2021-03", 2),
                            ("repo_1","2021-01", 1),
                            ("repo_3","2021-04", 1),
                            ("repo_2","2021-02", 2)
        ]

        new_contributors_columns = ["repo_name","month", "count"]
        df_expected = spark.createDataFrame(data=new_contributors, schema = new_contributors_columns)

        self.assertListEqual(df_after.collect(), df_expected.collect())


if __name__ == '__main__':
    unittest.main()