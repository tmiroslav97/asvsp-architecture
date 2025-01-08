#!/usr/bin/python

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col, lit, expr
from pyspark.sql.types import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL - Cache and persist") \
    .getOrCreate()

quiet_logs(spark)

sc = spark.sparkContext

rdd = sc.textFile("/spark/examples/src/main/resources/people.csv")
rdd2 = rdd.map(lambda line: Row(line.split(";")))
rdd3 = rdd2.cache()
print(rdd3.count())

df = rdd3.toDF()
df2 = df.persist()
df2.show()
df2.unpersist()

