-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.rain_topic_kafka (
    data String
) ENGINE = Kafka('kafka:9092', 'rain', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.rain (
     name String,
     timestamp DATETIME64,
     value Float64,
     type String,
     latitude Float64,
     longitude Float64
) ENGINE = MergeTree()
      ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.rain_topic_mv TO innovacity.rain AS
SELECT
    JSONExtractString(data, 'name') AS sensor_name,
    toDateTime(JSONExtractString(data, 'timestamp')) AS timestamp,
    JSONExtractFloat(data, 'readings', 1) AS value, -- arrays start from 1
    JSONExtractString(data, 'type', 1) AS type,
    JSONExtractFloat(data, 'location', 'coordinates', 1) AS latitude,
    JSONExtractFloat(data, 'location', 'coordinates', 2) AS longitude
FROM innovacity.rain_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+

-- +--------------------------+
-- | START AGGREGATE 1 MINUTE |
-- +--------------------------+
CREATE TABLE innovacity.rain1m
(
    name String,
    timestamp1m DATETIME64,
    avgRain AggregateFunction(avgState, Float64), -- Using sumState for stateful aggregation
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, name, longitude, latitude);


CREATE MATERIALIZED VIEW innovacity.rain1m_mv
TO innovacity.rain1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    name,
    avgState(value) as avgRain,
    latitude,
    longitude
FROM innovacity.rain
GROUP BY (timestamp1m, name, latitude, longitude);
-- +------------------------+
-- | END AGGREGATE 1 MINUTE |
-- +------------------------+

-- +----------------------+
-- | START MOVING AVERAGE |
-- +----------------------+
CREATE TABLE innovacity.rain_ma (
    name String,
    timestamp1m DATETIME64,
    avgRain Float64,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (timestamp1m, name, latitude, longitude);

-- Creare una Materialized View
CREATE MATERIALIZED VIEW innovacity.rain1m_mov_avg
TO innovacity.rain_ma
AS
SELECT
    name,
    toStartOfMinute(timestamp) AS timestamp1m,
    avg(value) OVER (PARTITION BY name, toStartOfMinute(timestamp) ORDER BY timestamp1m ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avgRain,
    latitude,
    longitude
FROM innovacity.rain;
-- +--------------------+
-- | END MOVING AVERAGE |
-- +--------------------+
