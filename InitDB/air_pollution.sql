-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.air_pollution_topic_kafka
(
    data String
) ENGINE = Kafka('kafka:9092', 'air_pollution', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.air_pollution
(
    name      String,
    timestamp DATETIME64,
    value     Float64,
    type      String,
    latitude  Float64,
    longitude Float64
) ENGINE = MergeTree()
      ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.air_pollution_topic_mv TO innovacity.air_pollution AS
SELECT JSONExtractString(data, 'name')                       AS name,
       toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
       JSONExtractFloat(data, 'readings', 1, 'value')        AS value, -- arrays start from 1
       JSONExtractString(data, 'type')                       AS type,
       JSONExtractFloat(data, 'location', 'coordinates', 1)  AS latitude,
       JSONExtractFloat(data, 'location', 'coordinates', 2)  AS longitude
FROM innovacity.air_pollution_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+

-- +--------------------------+
-- | START AGGREGATE 1 MINUTE |
-- +--------------------------+
CREATE TABLE innovacity.air_pollution1m
(
    name        String,
    timestamp1m DATETIME64,
    avg_air_pollution AggregateFunction(avgState, Float64),
    latitude    Float64,
    longitude   Float64
) ENGINE = AggregatingMergeTree
      ORDER BY (timestamp1m, name, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.air_pollution1m_mv
    TO innovacity.air_pollution1m
AS
SELECT toStartOfMinute(timestamp) AS timestamp1m,
       name,
       avgState(value)            as avg_air_pollution,
       latitude,
       longitude
FROM innovacity.air_pollution
GROUP BY (timestamp1m, name, latitude, longitude);

-- +------------------------+
-- | END AGGREGATE 1 MINUTE |
-- +------------------------+

-- +----------------------+
-- | START MOVING AVERAGE |
-- +----------------------+
CREATE TABLE innovacity.air_pollution5m_overall
(
    timestamp5m       DATETIME64,
    avg_air_pollution Float64
) ENGINE = MergeTree()
      ORDER BY (timestamp5m);

CREATE MATERIALIZED VIEW innovacity.air_pollution_5m_overall_mv
    TO innovacity.air_pollution5m_overall
AS
SELECT toStartOfFiveMinute(timestamp) AS timestamp5m,
       avg(value)                     AS avg_air_pollution
FROM innovacity.air_pollution
GROUP BY timestamp5m
-- +--------------------+
-- | END MOVING AVERAGE |
-- +--------------------+