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
    .appName("Python Spark SQL - Join") \
    .getOrCreate()

quiet_logs(spark)

df = spark.range(0, 20)
print(df.rdd.getNumPartitions())

emp = [
  (1, "Smith", -1, "2018", "10", "M", 3000),
  (2, "Rose", 1, "2010", "20", "M", 4000),
  (3, "Williams", 1, "2010", "10", "M", 1000),
  (4, "Jones", 2, "2005", "10", "F", 2000),
  (5, "Brown", 2, "2010", "40", "", -1),
  (6, "Brown", 2, "2010", "50", "", -1)
]

empColumns = ["emp_id", "name", "superior_emp_id", "year_joined", "emp_dept_id", "gender", "salary"]
empDF = spark.sparkContext.parallelize(emp).toDF(empColumns).coalesce(2)
empDF.show(truncate=False)
print(empDF.rdd.getNumPartitions())

dept = [
  ("Finance", 10),
  ("Marketing", 20),
  ("Sales", 30),
  ("IT", 40)
]

deptColumns = ["dept_name", "dept_id"]
deptDF = spark.sparkContext.parallelize(dept).toDF(deptColumns).coalesce(2)
deptDF.show(truncate=False)
print(deptDF.rdd.getNumPartitions())

empDF.join(deptDF, empDF["emp_dept_id"] == deptDF["dept_id"], "inner").show(truncate=False)

