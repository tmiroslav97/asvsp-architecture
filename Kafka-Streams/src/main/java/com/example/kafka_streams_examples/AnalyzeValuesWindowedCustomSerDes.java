package com.example.kafka_streams_examples;

import java.util.Map;
import java.util.Properties;

import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.Grouped;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Materialized;
import org.apache.kafka.streams.kstream.Produced;
import org.apache.kafka.streams.kstream.TimeWindows;
import org.apache.kafka.streams.kstream.Windowed;
import org.apache.kafka.streams.kstream.WindowedSerdes;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.time.Duration;

// Racuna Avg za sve istorijske podatke NA NIVOU ZADATOG VREMENSKOG OKVIRA, pa potom za sve novopridosle podatke isto tako
// miner-average-hash-rate-3
// analyze-values-windowed-custom-serdes-app-KSTREAM-AGGREGATE-STATE-STORE-0000000005-changelog -- tu su lepo serijalizovani podaci
public class AnalyzeValuesWindowedCustomSerDes {

    private static final ObjectMapper MAPPER = new ObjectMapper();
    public static void main(String[] args) {

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "analyze-values-windowed-custom-serdes-app");
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

        TimeWindows slidingWindow = TimeWindows.ofSizeAndGrace(Duration.ofMinutes(1), Duration.ofSeconds(10));

        KTable<Windowed<String>, Double> avgHashRate = hashRates
            .groupBy((key, value) -> "MINER_STATS", Grouped.with(Serdes.String(), Serdes.Double()))
            .windowedBy(slidingWindow)
            .aggregate(
                () -> new HashAccumulator(0.0, 0),
                (key, newValue, aggregate) -> {
                    aggregate.sum += newValue;
                    aggregate.count++;
                    return aggregate;
                },
                Materialized.with(Serdes.String(), new HashAccumulatorSerdes())
            )
            .mapValues(agg -> agg.sum / agg.count);

        avgHashRate.toStream().to("miner-average-hash-rate-3", Produced.with(WindowedSerdes.timeWindowedSerdeFrom(String.class, 60000L), Serdes.Double())); // kafka-ui ne moze da vidi deserijalizuje double vrednosti -- https://gregstoll.com/~gregstoll/floattohex/ :)

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }

    public static class HashAccumulator {
        public double sum;
        public int count;
        public HashAccumulator() {}
        public HashAccumulator(double sum, int count) { this.sum = sum; this.count = count; }
    }

    public static class HashAccumulatorSerdes implements Serde<HashAccumulator> {

        public Serializer<HashAccumulator> serializer() {
            return new HashAccumulatorSerializerDeserializer();
        }

        public Deserializer<HashAccumulator> deserializer() {
            return new HashAccumulatorSerializerDeserializer();
        }

    }

    public static class HashAccumulatorSerializerDeserializer implements Serializer<HashAccumulator>, Deserializer<HashAccumulator> {
        private final ObjectMapper objectMapper = new ObjectMapper();

        public HashAccumulatorSerializerDeserializer() {
        }

        @Override
        public void configure(Map<String, ?> props, boolean isKey) {
        }

        @Override
        public byte[] serialize(String topic, HashAccumulator data) {
            if (data == null)
                return null;

            try {
                return objectMapper.writeValueAsBytes(data);
            } catch (Exception e) {
                throw new SerializationException("Error serializing message", e);
            }
        }

        @Override
        public HashAccumulator deserialize(String topic, byte[] bytes) {
            if (bytes == null)
                return null;

            HashAccumulator data;
            try {
                data = objectMapper.readValue(bytes, HashAccumulator.class);
            } catch (Exception e) {
                throw new SerializationException(e);
            }

            return data;
        }

        @Override
        public void close() {
        }
    }
}
