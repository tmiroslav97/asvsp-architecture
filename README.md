# ASVSP

## Osnovne informacije

Projekat je napravljen za potrebe predmeta arhitekture sistema velikih skupova podataka. Ideja je da se u toku semestra na terminima vježbi uvede jedan po jedan servis koji čini ovaj projekat. Cjelokupan projekat (klaster) napravljen je tako da predstavlja zaokruženu cjelinu onoga što se sa praktične strane obrađuje na predmetu i da posluži kao primjer kako bi trebala da izgleda arhitektura projekta kojeg studenti implementiraju na predmetu.

**Napomena:**
* Zbog različitih okruženja u laboratoriji i na personalnim računarima održavaće se dvije odvojene grane
    * main - za upotrebu na personalnim računarima
    * classroom - za upotrebu na računarima u laboratoriji

## Klaster

Klaster se pokreće tako što se nakon pozicioniranja u root projekta unutar terminala (linux terminal, git bash, powershell i sl.) unese parametrizovana naredba:

```./scripts/cluster_up.sh <list_of_services>```

Argument <list_of_services> je obavezan i ukoliko se ne navede nijedan servis koji čini ovaj klaster neće biti pokrenut. Moguće vrijednosti su: hdfs, hue, hive, spark, airflow, metabase, kafka, data_generator, locust i simple_kafka_consumer. Navedene vrijednosti se odnose na sledeće servise u klasteru:
* hdfs - Hadoop
* hue - Hue
* hive - Hive
* spark - Apache-Spark
* airflow - Airflow
* metabase - Metabase
* kafka - Kafka
* data_generator - Data-Generator
* locust - Locust
* simple_kafka_consumer - Simple-Kafka-Consumer

Klaster se gasi tako što se nakon pozicioniranja u root projekta unutar terminala (linux terminal, git bash, powershell i sl.) unese naredba koja će da ugasi sve pokrenute servise u klasteru i opciono da obriše sve docker kontejnere vezane za servise:

```./scripts/cluster_down.sh```

**Napomena:**
* zbog problema sa permisijama unutar konfiguracionog direktorijuma servisa Hue, zakomentarisan je bind mount volume na konfiguracioni direktorijum i uveden je Dockerfile tako da se konfiguracija odmah prekopira u trenutku pravljenja docker slike. Ukoliko postoji potreba da se prekonfiguriše Hue, potrebno je ponovo kreirati sliku ili opciono pronaći drugi način kako da se ovaj problem premosti (putem docker volume i sl.)

## Dodatne naredbe

Sve bash skripte unutar projekta treba da imaju odgovarajuće permisije ako se radi na Linux/Max mašini:

```find . -type -iname "*.sh" -exec chmod +x {} \;```

Ako se javljaju problemi sa završekom linije (CLRF vs LF):

```find . -type -iname "*.sh" -exec sed -i -e 's/\r$//' {} \;```