CREATE TABLE fondacije_part (
   Naziv STRING,
   MaticniBroj INT,
   IdentifikatorMesta INT,
   SifraDelatnosti INT, 
   DatumRegistracije STRING
)
PARTITIONED BY (
    GodReg STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

set hive.exec.dynamic.partition=true;                                                                           
set hive.exec.dynamic.partition.mode=nonstrict;

INSERT INTO fondacije_part
PARTITION(GodReg)
SELECT *, SUBSTR(DatumRegistracije, 1, 4) AS GodReg
FROM fondacije;