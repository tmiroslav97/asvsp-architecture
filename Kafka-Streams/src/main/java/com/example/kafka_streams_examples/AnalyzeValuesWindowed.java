package com.example.kafka_streams_examples;

import java.util.Properties;
import java.time.Duration;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;


// Racuna Avg za sve istorijske podatke NA NIVOU ZADATOG VREMENSKOG OKVIRA, pa potom za sve novopridosle podatke isto tako
// miner-average-hash-rate-2
// analyze-values-windowed-app-KSTREAM-AGGREGATE-STATE-STORE-0000000005-changelog
// obratiti paznju na kljuc poruke - automatski se doda timestamp u binarnom obliku
public class AnalyzeValuesWindowed {

    private static final ObjectMapper MAPPER = new ObjectMapper();
    public static void main(String[] args) {

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "analyze-values-windowed-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> input =
                builder.stream("network_data", Consumed.with(Serdes.String(), Serdes.String()));

        KStream<String, String> filteredPackets = input.filter((key, jsonString) -> {
            try {
                JsonNode root = MAPPER.readTree(jsonString);
                String ipDst = root.path("payload").path("src").asText();
                return ipDst.equals("192.168.68.105");
            } catch (Exception e) {
                return false;
            }
        });

        KStream<String, Double> hashRates = filteredPackets.mapValues(value -> {
            try {
                JsonNode root = MAPPER.readTree(value);
                String innerJsonStr = root.at("/payload/payload/payload/load").asText();

                JsonNode stats = MAPPER.readTree(innerJsonStr);
                String rawHashRate = stats.get("HashRate").asText();

                return Double.parseDouble(rawHashRate.replace("MH/s", ""));
            } catch (Exception e) {
                return null;
            }
        }).filter((k, v) -> v != null);

        TimeWindows hoppingWindow = TimeWindows.ofSizeAndGrace(Duration.ofMinutes(1), Duration.ofSeconds(10)).advanceBy(Duration.ofSeconds(15));
        // TimeWindows tumblingWindow = TimeWindows.ofSizeAndGrace(Duration.ofMinutes(1), Duration.ofSeconds(10));
        // SessionWindows sessionWindow = SessionWindows.ofInactivityGapAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1));
        // SlidingWindows slidingWindow = SlidingWindows.ofTimeDifferenceAndGrace(Duration.ofMinutes(30), Duration.ofMinutes(5));

        KTable<Windowed<String>, String> aggregatedStats = hashRates
            .groupBy((key, value) -> "MINER_STATS", Grouped.with(Serdes.String(), Serdes.Double()))
            .windowedBy(hoppingWindow)
            .aggregate(
                () -> "0.0,0", // Initializer: "sum,count"
                (key, newValue, aggregate) -> {
                    String[] parts = aggregate.split(",");
                    double currentSum = Double.parseDouble(parts[0]) + newValue;
                    int currentCount = Integer.parseInt(parts[1]) + 1;
                    return currentSum + "," + currentCount;
                },
                Materialized.with(Serdes.String(), Serdes.String())
            );

        aggregatedStats.toStream()
            .mapValues(aggValue -> {
                String[] parts = aggValue.split(",");
                double avg = Double.parseDouble(parts[0]) / Double.parseDouble(parts[1]);
                return String.format("%.4f MH/s", avg);
            })
            .to("miner-average-hash-rate-2", Produced.with(WindowedSerdes.timeWindowedSerdeFrom(String.class, 60000L), Serdes.String()));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }

}
