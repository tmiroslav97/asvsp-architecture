#!/usr/bin/python

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import isnull, when, count, col
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("Python Spark ML example - Titanic") \
    .getOrCreate()

quiet_logs(spark)

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]

df = spark.read.format("csv").option('header', 'true').load(HDFS_NAMENODE + "/user/test/titanic/train.csv")

df.show(5)
print(df.count())
print(df.columns)
print(df.dtypes)

dataset = df.select(col('Survived').cast('float'),
                    col('Pclass').cast('float'),
                    col('Sex'),
                    col('Age').cast('float'),
                    col('Fare').cast('float'),
                    col('Embarked')
            )
dataset.show(5)

dataset.select([count(when(isnull(c), c)).alias(c) for c in dataset.columns]).show()

dataset = dataset.replace('?', None).dropna(how='any')

dataset = StringIndexer(
    inputCol='Sex', 
    outputCol='Gender', 
    handleInvalid='keep').fit(dataset).transform(dataset)

dataset = StringIndexer(
    inputCol='Embarked', 
    outputCol='Boarded', 
    handleInvalid='keep').fit(dataset).transform(dataset)
    
dataset.show()

dataset = dataset.drop('Sex')
dataset = dataset.drop('Embarked')

# Assemble all the features with VectorAssembler
required_features = [
    'Pclass',
    'Age',
    'Fare',
    'Gender',
    'Boarded'
]

assembler = VectorAssembler(inputCols=required_features, outputCol='features')
transformed_data = assembler.transform(dataset)

(training_data, test_data) = transformed_data.randomSplit([0.8,0.2])

rf = RandomForestClassifier(labelCol='Survived', 
                            featuresCol='features',
                            maxDepth=5)

model = rf.fit(training_data)
predictions = model.transform(test_data)

evaluator = MulticlassClassificationEvaluator(
    labelCol='Survived', 
    predictionCol='prediction', 
    metricName='accuracy')

accuracy = evaluator.evaluate(predictions)
print('Test Accuracy = ', accuracy)

