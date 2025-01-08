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
    .appName("Python Spark SQL - Add, remove, or rename columns") \
    .getOrCreate()

quiet_logs(spark)

data = [
    Row(Row("James","","Smith"),"36636","M","3000"),
    Row(Row("Michael","Rose",""),"40288","M","4000"),
    Row(Row("Robert","","Williams"),"42114","M","4000"),
    Row(Row("Maria","Anne","Jones"),"39192","F","4000"),
    Row(Row("Jen","Mary","Brown"),"","F","-1")
]

schema = StructType() \
    .add("name", StructType() \
        .add("firstname", StringType()) \
        .add("middlename", StringType()) \
        .add("lastname", StringType())) \
    .add("id", StringType()) \
    .add("gender", StringType()) \
    .add("salary", StringType())

df = spark.createDataFrame(spark.sparkContext.parallelize(data), schema)

df = df.withColumn("Country", lit("USA")).withColumn("anotherColumn", lit("anotherValue"))

df.printSchema()
df.show(truncate=False)

df = df.withColumn("salary", col("salary")*100)
df.show(truncate=False)

df = df.drop("anotherColumn").drop("Country")
df.show(truncate=False)