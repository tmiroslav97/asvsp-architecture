CREATE EXTERNAL TABLE star (
   charge  DOUBLE,
   clus    DOUBLE,
   dst     DOUBLE,
   enumber DOUBLE,
   etime   DOUBLE,
   hist    DOUBLE,
   nlb     DOUBLE,
   qxb     DOUBLE,
   rnumber DOUBLE,
   tracks  DOUBLE,
   vertex  DOUBLE,
   zdc     DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/test/star';

SELECT *
FROM star
LIMIT 20;

CREATE TABLE star_parquet (
   charge  DOUBLE,
   clus    DOUBLE,
   dst     DOUBLE,
   enumber DOUBLE,
   etime   DOUBLE,
   hist    DOUBLE,
   nlb     DOUBLE,
   qxb     DOUBLE,
   rnumber DOUBLE,
   tracks  DOUBLE,
   vertex  DOUBLE,
   zdc     DOUBLE
)
STORED AS PARQUET;

INSERT INTO star_parquet
SELECT *
FROM star;

SELECT *
FROM star_parquet
LIMIT 20;