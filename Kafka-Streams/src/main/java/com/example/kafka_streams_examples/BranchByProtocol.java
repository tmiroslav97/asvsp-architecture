package com.example.kafka_streams_examples;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;

import java.util.Properties;
import java.util.Map;

public class BranchByProtocol {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private static boolean isTcp(String key, String value) {
        return hasLayerType(value, "TCP");
    }

    private static boolean isUdp(String key, String value) {
        return hasLayerType(value, "UDP");
    }

    private static boolean hasLayerType(String json, String expected) {
        try {
            JsonNode root = MAPPER.readTree(json);

            // Ether → IP → TCP/UDP
            JsonNode protocolLayer =
                    root.path("payload")
                        .path("payload")
                        .path("layer_type");

            return expected.equals(protocolLayer.asText());
        } catch (Exception e) {
            return false;
        }
    }

    public static void main(String[] args) {

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "protocol-branching-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> input =
                builder.stream("network_data", Consumed.with(Serdes.String(), Serdes.String()));

        BranchedKStream<String, String> branchedStream = input.split(Named.as("protocol-"));

        Map<String, KStream<String, String>> branches = branchedStream
            .branch(BranchByProtocol::isTcp, Branched.as("tcp"))
            .branch(BranchByProtocol::isUdp, Branched.as("udp"))
            .defaultBranch(Branched.as("other")); 

        KStream<String, String> tcpStream = branches.get("protocol-tcp");
        KStream<String, String> udpStream = branches.get("protocol-udp");

        tcpStream.to("packets-tcp", Produced.with(Serdes.String(), Serdes.String()));
        udpStream.to("packets-udp", Produced.with(Serdes.String(), Serdes.String()));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
