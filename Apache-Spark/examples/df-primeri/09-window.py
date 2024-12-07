#!/usr/bin/python

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL - Windowing") \
    .getOrCreate()

quiet_logs(spark)

simpleData = [
    ("James", "Sales", 3000),
    ("Michael", "Sales", 4600),
    ("Robert", "Sales", 4100),
    ("Maria", "Finance", 3000),
    ("James", "Sales", 3000),
    ("Scott", "Finance", 3300),
    ("Jen", "Finance", 3900),
    ("Jeff", "Marketing", 3000),
    ("Kumar", "Marketing", 2000),
    ("Saif", "Sales", 4100)
]

df = spark.sparkContext.parallelize(simpleData).toDF(["employee_name", "department", "salary"])
df.show()

windowSpec = Window.partitionBy("department").orderBy("salary")
df.withColumn("row_number", row_number().over(windowSpec)).show()
df.withColumn("dense_rank", dense_rank().over(windowSpec)).show()
df.withColumn("rank", rank().over(windowSpec)).show()

df.withColumn("lag", lag("salary", 2).over(windowSpec)).show()
