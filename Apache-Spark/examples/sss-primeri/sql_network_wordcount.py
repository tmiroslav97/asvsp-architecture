r"""
 To run this on your local machine, you need to first run a Netcat server
    `$ netcat -vvl -p 5858`
 and then run the example
    `$SPARK_HOME/bin/spark-submit spark/primeri/sql_network_wordcount.py localhost 5858`
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getRootLogger().setLevel(logger.Level.WARN)

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

words.createOrReplaceTempView("words_temp_view")

wordCounts = \
                spark.sql("select word, count(*) as total from words_temp_view group by word order by total desc limit 10")


query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()