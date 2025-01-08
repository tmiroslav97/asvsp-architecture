#!/usr/bin/python

# apk update
# apk add make automake gcc g++ subversion python3-dev
# pip3 install numpy

from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.ml.regression import LinearRegression, RegressionEvaluator


def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark ML example") \
    .getOrCreate()

quiet_logs(spark)

# Use the Spark CSV datasource with options specifying:
# - First line of file is a header
# - Automatically infer the schema of the data
data = spark.read.format("csv") \
  .option("header", "true") \
  .option("inferSchema", "true") \ 
  .load("/databricks-datasets/samples/population-vs-price/data_geo.csv")

data.cache() # Cache data for faster reuse

data = data.dropna() # drop rows with missing values
exprs = [col(column).alias(column.replace(' ', '_')) for column in data.columns]

spark.udf.register("oneElementVec", lambda d: Vectors.dense([d]), returnType=VectorUDT())
tdata = data.select(*exprs).selectExpr("oneElementVec(2014_Population_estimate) as features", "2015_median_sales_price as label")

# Define LinearRegression algorithm
lr = LinearRegression()

# Fit 2 models, using different regularization parameters
modelA = lr.fit(data, {lr.regParam:0.0})
modelB = lr.fit(data, {lr.regParam:100.0})

# Make predictions
predictionsA = modelA.transform(data)

evaluator = RegressionEvaluator(metricName="rmse")
RMSE = evaluator.evaluate(predictionsA)
print("ModelA: Root Mean Squared Error = " + str(RMSE))
# ModelA: Root Mean Squared Error = 128.602026843

predictionsB = modelB.transform(data)
RMSE = evaluator.evaluate(predictionsB)
print("ModelB: Root Mean Squared Error = " + str(RMSE))
# ModelB: Root Mean Squared Error = 129.496300193