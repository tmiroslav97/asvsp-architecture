#!/usr/bin/python

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col, lit, array_contains
from pyspark.sql.types import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL - Filter/where") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

quiet_logs(spark)

arrayStructureData = [
    Row(Row("James", "", "Smith"), ["Java", "Scala", "C++"], "OH", "M"),
    Row(Row("Anna", "Rose", ""), ["Spark", "Java", "C++"], "NY", "F"),
    Row(Row("Julia", "", "Williams"), ["CSharp", "VB"], "OH", "F"),
    Row(Row("Maria", "Anne", "Jones"), ["CSharp", "VB"], "NY", "M"),
    Row(Row("Jen", "Mary", "Brown"), ["CSharp", "VB"], "NY", "M"),
    Row(Row("Mike", "Mary", "Williams"), ["Python", "VB"], "OH", "M")
]

arrayStructureSchema = StructType() \
    .add("name", StructType() \
        .add("firstname", StringType()) \
        .add("middlename", StringType()) \
        .add("lastname", StringType())) \
    .add("languages", ArrayType(StringType())) \
    .add("state", StringType()) \
    .add("gender", StringType())

df = spark.createDataFrame(
    spark.sparkContext.parallelize(arrayStructureData), arrayStructureSchema)
df.printSchema()
df.show()

df.filter(df["state"] == "OH").show(truncate=False)
df.filter(col("state") == "OH").show(truncate=False)
df.filter("gender == 'M'").show(truncate=False)
# df.where("gender == 'M'").show(truncate=False)

### Visestruki uslovi
df.filter((df["state"] == "OH") & (df["gender"] == "M")).show(truncate=False)

### Sadrzaj niza
df.filter(array_contains(df["languages"], "Java")).show(truncate=False)

### Ugnjezdena polja
df.filter(df["name.lastname"] == "Williams").show(truncate=False)
