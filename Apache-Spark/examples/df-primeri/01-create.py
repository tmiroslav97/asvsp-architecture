#!/usr/bin/python

import os
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col
from pyspark.sql.types import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL - Create DataFrame") \
    .getOrCreate()

quiet_logs(spark)

### Kreiranje RDD od niza
rdd = spark.sparkContext.parallelize(
        [("Java", 20000), 
        ("Python", 100000), 
        ("Scala", 3000)])
rdd.foreach(lambda x : print(x))

### DataFrame od RDD
dfFromRDD1 = rdd.toDF()
dfFromRDD1.printSchema()

### DataFrame od RDD sa imenima kolona
dfFromRDD2 = rdd.toDF(["language", "users_count"])
dfFromRDD2.printSchema()

### DataFrame od RDD sa shemom
schema = StructType([
                 StructField("language", StringType(), True),
                 StructField("users_count", IntegerType(), True)
          ])
rowRDD = rdd.map(lambda attributes : Row(attributes[0], attributes[1]))

dfFromRDD3 = spark.createDataFrame(rowRDD, schema)
dfFromRDD3.printSchema()
dfFromRDD3.show()

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]

### DataFrame od JSON fajla
dfFromJSON = spark.read.option("multiline", "true").json(HDFS_NAMENODE + "/user/test/example.json")
dfFromJSON.printSchema()
dfFromJSON.show()

### DataFrame od Parquet fajla
dfParquetJSON = spark.read.parquet(HDFS_NAMENODE + "/user/test/parquet-example")
dfParquetJSON.printSchema()
dfParquetJSON.show(10)