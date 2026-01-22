package com.example.kafka_streams_examples;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;

import java.util.Properties;

public class FilterByIP {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) {

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "filter-by-ip-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> input =
                builder.stream("network_data", Consumed.with(Serdes.String(), Serdes.String()));

        KStream<String, String> filteredPackets = input.filter((key, jsonString) -> {
            try {
                JsonNode root = MAPPER.readTree(jsonString);
                String ipDst = root.path("payload").path("dst").asText();
                return !ipDst.equals("192.168.65.1");
            } catch (Exception e) {
                return false;
            }
        });

        filteredPackets.to("filtered-ip", Produced.with(Serdes.String(), Serdes.String()));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
