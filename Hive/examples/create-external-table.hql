--beeline -u jdbc:hive2://localhost:10000

CREATE DATABASE nvo;

USE nvo;

CREATE EXTERNAL TABLE fondacije (
   Naziv STRING,
   MaticniBroj INT,
   IdentifikatorMesta INT,
   SifraDelatnosti INT, 
   DatumRegistracije STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/user/test/fondacije'
tblproperties("skip.header.line.count"="1");

SELECT *
FROM fondacije
LIMIT 10;

