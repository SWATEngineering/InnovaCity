-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.temperatures_topic_kafka (
    data String
) ENGINE = Kafka('kafka:9092', 'temperature', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.temperatures (
    name String,
    timestamp DATETIME64,
    value Float64,
    type String,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.temperatures_topic_mv TO innovacity.temperatures AS
SELECT
    JSONExtractString(data, 'name') AS name,
    toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
    JSONExtractFloat(data, 'readings', 1, 'value') AS value, -- arrays start from 1
    JSONExtractString(data, 'type') AS type,
    JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
    JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.temperatures_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+

-- +--------------------------+
-- | START AGGREGATE 1 MINUTE |
-- +--------------------------+
CREATE TABLE innovacity.temperatures1m
(
    name String,
    timestamp1m DATETIME64,
    avgTemperature AggregateFunction(avgState, Float64),
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, name, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.temperatures1m_mv
TO innovacity.temperatures1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    name,
    avgState(value) as avgTemperature,
    latitude,
    longitude
FROM innovacity.temperatures
GROUP BY (timestamp1m, name, latitude, longitude);

CREATE TABLE innovacity.temperatures_ma (
    name String,
    timestamp1m DATETIME64,
    avgTemperature Float64,
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
CREATE MATERIALIZED VIEW innovacity.temperatures1m_mov_avg
TO innovacity.temperatures_ma
AS
SELECT
    name,
    toStartOfMinute(timestamp) AS timestamp1m,
    avg(value) OVER (PARTITION BY  toStartOfMinute(timestamp) ORDER BY timestamp1m ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avgTemperature,
    latitude,
    longitude
FROM innovacity.temperatures;
-- +--------------------+
-- | END MOVING AVERAGE |
-- +--------------------+