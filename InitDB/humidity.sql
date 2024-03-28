-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.humidity_topic_kafka
(
    data String
) ENGINE = Kafka('kafka:9092', 'humidity', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.humidity
(
    name      String,
    timestamp DATETIME64,
    value     Float64,
    type      String,
    latitude  Float64,
    longitude Float64
) ENGINE = MergeTree()
      ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.humidity_topic_mv TO innovacity.humidity AS
SELECT JSONExtractString(data, 'name')                       AS name,
       toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
       JSONExtractFloat(data, 'readings', 1, 'value')        AS value, -- arrays start from 1
       JSONExtractString(data, 'type')                       AS type,
       JSONExtractFloat(data, 'location', 'coordinates', 1)  AS latitude,
       JSONExtractFloat(data, 'location', 'coordinates', 2)  AS longitude
FROM innovacity.humidity_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+

-- +--------------------------+
-- | START AGGREGATE 1 MINUTE |
-- +--------------------------+
CREATE TABLE innovacity.humidity1m
(
    name        String,
    timestamp1m DATETIME64,
    avgHumidity AggregateFunction(avgState, Float64),
    latitude    Float64,
    longitude   Float64
)
    ENGINE = AggregatingMergeTree
        ORDER BY (timestamp1m, name, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.humidity1m_mv
    TO innovacity.humidity1m
AS
SELECT toStartOfMinute(timestamp) AS timestamp1m,
       name,
       avgState(value)            as avgHumidity,
       latitude,
       longitude
FROM innovacity.humidity
GROUP BY (timestamp1m, name, latitude, longitude);

-- +------------------------+
-- | END AGGREGATE 1 MINUTE |
-- +------------------------+

-- +----------------------+
-- | START MOVING AVERAGE |
-- +----------------------+
CREATE TABLE innovacity.humidity5m_overall
(
    timestamp5m DATETIME64,
    avgHumidity Float64
) ENGINE = MergeTree()
      ORDER BY (timestamp5m);

CREATE MATERIALIZED VIEW innovacity.humidity_5m_overall_mv
    TO innovacity.humidity5m_overall
AS
SELECT toStartOfFiveMinute(timestamp) AS timestamp5m,
       avg(value)                     AS avgHumidity
FROM innovacity.humidity
GROUP BY timestamp5m;
-- +--------------------+
-- | END MOVING AVERAGE |
-- +--------------------+