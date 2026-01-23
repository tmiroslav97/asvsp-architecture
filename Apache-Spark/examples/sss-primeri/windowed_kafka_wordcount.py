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

# izracunavanja se vrse na svakih 30 sekundi, i uzimaju u obzir reči nastale u prethodnih minut
wordCounts = words.groupBy(window(words.timestamp, "1 minute", "30 seconds"), "word") \
                  .count().orderBy(desc("count")).limit(10).orderBy("window")

# primer kotrljajuceg okvira
# wordCounts = words.groupBy(window(words.timestamp, "30 seconds"), "word") \
#                   .count().orderBy(desc("count")).limit(10).orderBy("window")

query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()