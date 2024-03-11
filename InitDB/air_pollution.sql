-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.air_pollution_topic_kafka (
    data String
) ENGINE = Kafka('kafka:9092', 'air_pollution', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.air_pollution (
    name String,
    timestamp DATETIME64,
    value Float64,
    type String,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.air_pollution_topic_mv TO innovacity.air_pollution AS
SELECT
    JSONExtractString(data, 'name') AS name,
    toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
    JSONExtractFloat(data, 'readings', 1, 'value') AS value, -- arrays start from 1
    JSONExtractString(data, 'type') AS type,
    JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
    JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.air_pollution_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+

-- +--------------------------+
-- | START AGGREGATE 1 MINUTE |
-- +--------------------------+
CREATE TABLE innovacity.air_pollution1m
(
    name String,
    timestamp1m DATETIME64,
    avgair_pollution AggregateFunction(avgState, Float64),
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, name, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.air_pollution1m_mv
TO innovacity.air_pollution1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    name,
    avgState(value) as avgair_pollution,
    latitude,
    longitude
FROM innovacity.air_pollution
GROUP BY (timestamp1m, name, latitude, longitude);

CREATE TABLE innovacity.air_pollution_ma (
    name String,
    timestamp1m DATETIME64,
    avgair_pollution Float64,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (timestamp1m, name, latitude, longitude);
-- +------------------------+
-- | END AGGREGATE 1 MINUTE |
-- +------------------------+

-- +----------------------+
-- | START MOVING AVERAGE |
-- +----------------------+
CREATE MATERIALIZED VIEW innovacity.air_pollution1m_mov_avg
TO innovacity.air_pollution_ma
AS
SELECT
    name,
    toStartOfMinute(timestamp) AS timestamp1m,
    avg(value) OVER (PARTITION BY  toStartOfMinute(timestamp) ORDER BY timestamp1m ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avgair_pollution,
    latitude,
    longitude
FROM innovacity.air_pollution;
-- +--------------------+
-- | END MOVING AVERAGE |
-- +--------------------+