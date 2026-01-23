from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

spark = SparkSession \
    .builder \
    .appName("SSS - Network Wordcount") \
    .getOrCreate()

quiet_logs(spark)

sentences = spark \
  .readStream \
  .format("socket") \
  .option("host", "localhost") \
  .option("port", "5858") \
  .load()


words = sentences.select(
   explode(
       split(sentences.value, " ")
   ).alias("word")
)

wordCounts = words.groupBy("word").count().orderBy(desc("count")).limit(10)

query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()