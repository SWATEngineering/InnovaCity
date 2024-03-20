-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.parking_topic_kafka (
                                                     data String
) ENGINE = Kafka('kafka:9092', 'parking', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.parking (
                                         name String,
                                         timestamp DATETIME64,
                                         current Int32,
                                         max_slots Int32,
                                         type String,
                                         latitude Float64,
                                         longitude Float64
) ENGINE = MergeTree()
      ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.parking_topic_mv TO innovacity.parking AS
SELECT
    JSONExtractString(data, 'name') AS name,
    toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
    JSONExtractFloat(data, 'readings', 1, 'value') AS current, -- arrays start from 1
    JSONExtractFloat(data, 'readings', 2, 'value') AS max_slots,
    JSONExtractString(data, 'type') AS type,
    JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
    JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.parking_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+
