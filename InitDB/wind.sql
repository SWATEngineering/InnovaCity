-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.wind_topic_kafka
(
    data String
) ENGINE = Kafka('kafka:9092', 'wind', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.wind
(
    name      String,
    timestamp DATETIME64,
    value     Float64,
    type      String,
    direction UInt16,
    latitude  Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (name, timestamp);

CREATE
MATERIALIZED VIEW innovacity.wind_topic_mv TO innovacity.wind AS
SELECT JSONExtractString(data, 'name') AS name,
       toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
    JSONExtractFloat(data, 'readings', 1, 'value') AS value, -- arrays start from 1
    JSONExtractInt(data, 'readings', 2, 'value') AS direction,
    JSONExtractString(data, 'type') AS type,
    JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
    JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.wind_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+
