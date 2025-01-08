#!/usr/bin/python

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import *
from pyspark.sql.types import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL - Aggregation") \
    .getOrCreate()

quiet_logs(spark)

simpleData = [
    ("James","Sales","NY",90000,34,10000),
    ("Michael","Sales","NY",86000,56,20000),
    ("Robert","Sales","CA",81000,30,23000),
    ("Maria","Finance","CA",90000,24,23000),
    ("Raman","Finance","CA",99000,40,24000),
    ("Scott","Finance","NY",83000,36,19000),
    ("Jen","Finance","NY",79000,53,15000),
    ("Jeff","Marketing","CA",80000,25,18000),
    ("Kumar","Marketing","NY",91000,50,21000)
]
df = spark.sparkContext.parallelize(simpleData).toDF(["employee_name","department","state","salary","age","bonus"])
df.show()

print("approx_count_distinct: " + str(df.select(approx_count_distinct("salary")).collect()[0][0]))

df.select(collect_set("salary")).show(truncate=False)

df.select(first("salary")).show(truncate=False)

df.groupBy("department") \
    .agg(
        sum(col("salary")).alias("sum_salary"),
        avg(col("salary")).alias("avg_salary"),
        sum(col("bonus")).alias("sum_bonus"),
        avg(col("bonus")).alias("avg_bonus")
    ).show(truncate=False)