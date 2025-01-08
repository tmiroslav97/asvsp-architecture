CREATE TABLE fondacije_parquet (
   Naziv STRING,
   MaticniBroj INT,
   IdentifikatorMesta INT,
   SifraDelatnosti INT, 
   DatumRegistracije STRING
)
PARTITIONED BY (
    GodReg STRING
)
STORED AS PARQUET;

set hive.exec.dynamic.partition=true;                                                                           
set hive.exec.dynamic.partition.mode=nonstrict;

INSERT INTO fondacije_parquet
PARTITION(GodReg)
SELECT *, SUBSTR(DatumRegistracije, 1, 4) AS GodReg
FROM fondacije;