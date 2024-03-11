-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.ebike_topic_kafka (
    data String
) ENGINE = Kafka('kafka:9092', 'electric_bicycle', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.ebikes (
     name String,
     timestamp DATETIME64,
     value Float64,
     type String,
     latitude Float64,
     longitude Float64
) ENGINE = MergeTree()
      ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.ebike_topic_mv TO innovacity.ebikes AS
SELECT
    JSONExtractString(data, 'name') AS name,
    toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
    JSONExtractFloat(data, 'readings', 1, 'value') AS value,
    JSONExtractString(data, 'type') AS type,
    JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
    JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.ebike_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+


-- +--------------------------+
-- | START AGGREGATE 1 MINUTE |
-- +--------------------------+
CREATE TABLE innovacity.ebikes1m
(
    name String,
    timestamp1m DATETIME64,
    avgEBike AggregateFunction(avgState, Float64),
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, name, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.ebikes1m_mv
TO innovacity.ebikes1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    name,
    avgState(value) as avgEBike,
    latitude,
    longitude
FROM innovacity.ebikes
GROUP BY (timestamp1m, name, latitude, longitude);

CREATE TABLE innovacity.ebikes_ma (
    name String,
    timestamp1m DATETIME64,
    avgEBike Float64,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (timestamp1m, name, latitude, longitude);
-- +------------------------+
-- | END AGGREGATE 1 MINUTE |
-- +------------------------+