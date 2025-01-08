#!/usr/bin/python

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col, lit
from pyspark.sql.types import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL - Data types") \
    .getOrCreate()

quiet_logs(spark)

strType = StringType()
print("json : " + strType.json())
print("simpleString : " + strType.simpleString())
print("typeName : " + strType.typeName())

rdd = spark.sparkContext.parallelize(
        [("Java", 20000), 
        ("Python", 100000), 
        ("Scala", 3000)])

df = rdd.toDF()
df.printSchema()
df.show()

df = df \
    .withColumn("language", col("_1").cast(StringType())) \
    .withColumn("number", col("_2").cast(IntegerType())) \
    .drop("_1").drop("_2")

df.printSchema()
df.show()

