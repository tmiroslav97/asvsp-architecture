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
    .appName("Python Spark SQL - Pivot") \
    .getOrCreate()

quiet_logs(spark)

data = [
    ("Banana",1000,"USA"), ("Carrots",1500,"USA"), ("Beans",1600,"USA"),
    ("Orange",2000,"USA"), ("Orange",2000,"USA"), ("Banana",400,"China"),
    ("Carrots",1200,"China"), ("Beans",1500,"China"), ("Orange",4000,"China"),
    ("Banana",2000,"Canada"), ("Carrots",2000,"Canada"), ("Beans",2000,"Mexico")
]

df = spark.sparkContext.parallelize(data).toDF(["Product","Amount","Country"])
df.show()

pivotDF = df.groupBy("Product").pivot("Country").sum("Amount")
pivotDF.show()

unPivotDF = pivotDF.select(
        col("Product"),
        expr("stack(4, 'CAN', Canada, 'CHN', China, 'MEX', Mexico) as (Country,Total)")
    ).where("Total is not null")
unPivotDF.show()