from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("SSS - Joins") \
    .getOrCreate()

quiet_logs(spark)


sentences = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "broker1:9092") \
  .option("subscribe", "local-sentences") \
  .load()

words = sentences.select(
   explode(
       split(sentences.value, " ")
   ).alias("word"),
  sentences.timestamp
)

keywords = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "broker1:9092") \
  .option("subscribe", "local-keywords") \
  .load().select(col("value").alias("word"), col("timestamp"))

joined_streams = words.join(keywords, "word")

query = joined_streams \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()