-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.traffic_topic_kafka (
    data String
) ENGINE = Kafka('kafka:9092', 'traffic', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.traffic (
    name String,
    timestamp DATETIME64,
    num_cars Int32,
    traffic_level String,
    avg_time Float64,
    type String,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.traffic_topic_mv TO innovacity.traffic AS
SELECT
    JSONExtractString(data, 'name') AS name,
    toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
    JSONExtractFloat(data, 'readings', 1, 'value') AS num_cars, -- arrays start from 1
    JSONExtractString(data, 'readings', 2, 'value') AS traffic_level,
    JSONExtractString(data, 'readings', 3, 'value') AS avg_time,
    JSONExtractString(data, 'type') AS type,
    JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
    JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.traffic_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+