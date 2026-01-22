package com.example.kafka_streams_examples;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;

import java.util.Properties;

public class CountByDestination {

    private static final ObjectMapper MAPPER = new ObjectMapper();


    public static void main(String[] args) {

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "count-by-destination-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> input =
                builder.stream("network_data", Consumed.with(Serdes.String(), Serdes.String()));

        input
            .mapValues(jsonString -> {
                try {
                    JsonNode root = MAPPER.readTree(jsonString);
                    return root.path("payload").path("dst").asText();
                } catch (Exception e) {
                    return "unknown";
                }
            })
            .groupBy((key, dstIp) -> dstIp)
            .count(Materialized.as("counts-store"))
            .toStream()
            .to("dst-ip-counts", Produced.with(Serdes.String(), Serdes.Long()));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
