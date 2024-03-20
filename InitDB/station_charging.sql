-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+

CREATE TABLE innovacity.charging_station_topic_kafka
(
    data String
) ENGINE = Kafka('kafka:9092', 'charging_station', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.charging_station
(
    name      String,
    timestamp DATETIME64,
    erogation_power     Float64,
    availability  UInt8, 
    type      String,
    latitude  Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.charging_station_topic_mv TO innovacity.charging_station AS
SELECT JSONExtractString(data, 'name') AS name,
       toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
       JSONExtractFloat(data, 'readings', 1, 'value') AS erogation_power,
       JSONExtractInt(data, 'readings', 2, 'value') AS availability,
       JSONExtractString(data, 'type') AS type,
       JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
       JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.charging_station_topic_kafka;