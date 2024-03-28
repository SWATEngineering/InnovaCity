-- +----------------------+
-- | START KAFKA CONSUMER |
-- +----------------------+
CREATE TABLE innovacity.rain_topic_kafka
(
    data String
) ENGINE = Kafka('kafka:9092', 'rain', 'ch_group_1', 'JSONAsString');

CREATE TABLE innovacity.rain
(
    name      String,
    timestamp DATETIME64,
    value     Float64,
    type      String,
    latitude  Float64,
    longitude Float64
) ENGINE = MergeTree()
      ORDER BY (name, timestamp);

CREATE MATERIALIZED VIEW innovacity.rain_topic_mv TO innovacity.rain AS
SELECT JSONExtractString(data, 'name')                       AS name,
       toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
       JSONExtractFloat(data, 'readings', 1, 'value')        AS value, -- arrays start from 1
       JSONExtractString(data, 'type')                       AS type,
       JSONExtractFloat(data, 'location', 'coordinates', 1)  AS latitude,
       JSONExtractFloat(data, 'location', 'coordinates', 2)  AS longitude
FROM innovacity.rain_topic_kafka;
-- +--------------------+
-- | END KAFKA CONSUMER |
-- +--------------------+

-- +--------------------------+
-- | START AGGREGATE 1 MINUTE |
-- +--------------------------+
CREATE TABLE innovacity.rain1m
(
    name                String,
    timestamp1m         DATETIME64,
    avgRain             Float64, -- Using sumState for stateful aggregation
    latitude            Float64,
    longitude           Float64,
    insertion_timestamp DATETIME DEFAULT now()
)
    ENGINE = AggregatingMergeTree
        ORDER BY (timestamp1m, name, longitude, latitude);


CREATE MATERIALIZED VIEW innovacity.rain1m_mv
    TO innovacity.rain1m
AS
SELECT toStartOfMinute(timestamp) AS timestamp1m,
       name,
       avg(value)                 as avgRain,
       latitude,
       longitude,
       now()                      AS insertion_timestamp
FROM innovacity.rain
GROUP BY (timestamp1m, name, latitude, longitude);
-- +------------------------+
-- | END AGGREGATE 1 MINUTE |
-- +------------------------+

-- +----------------------+
-- | START MOVING AVERAGE |
-- +----------------------+
CREATE TABLE innovacity.rain5m_overall
(
    timestamp5m         DATETIME64,
    avgRain             Float64,
    insertion_timestamp DATETIME DEFAULT now()
) ENGINE = MergeTree()
      ORDER BY (timestamp5m);

-- Creare una Materialized View
CREATE MATERIALIZED VIEW innovacity.rain_5m_overall_mv
    TO innovacity.rain5m_overall
AS
SELECT toStartOfFiveMinute(timestamp) AS timestamp5m,
       avg(value)                     AS avgRain,
       now()                          AS insertion_timestamp
FROM innovacity.rain
GROUP BY timestamp5m;
-- +--------------------+
-- | END MOVING AVERAGE |
-- +--------------------+
