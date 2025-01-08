CREATE TABLE fondacije_avro 
ROW FORMAT
SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS
INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
TBLPROPERTIES ('avro.schema.literal'='{
  "namespace": "testing.hive.avro.serde",
  "name": "fondacije",
  "type": "record",
  "fields": [
    { "name":"Naziv", "type":"string" },
    { "name":"MaticniBroj", "type":"int" },
    { "name":"IdentifikatorMesta", "type":"int" },
    { "name":"SifraDelatnosti", "type":"int" },
    { "name":"DatumRegistracije", "type":"string" }
  ]
}');

INSERT INTO fondacije_avro
SELECT *
FROM fondacije;
