CREATE TABLE innovacity.reservoirs_queue (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = Kafka('kafka:9092', 'reservoir', 'ch_group_1', 'JSONEachRow');

CREATE TABLE innovacity.reservoirs (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = MergeTree()
ORDER BY (nome_sensore, timestamp);

CREATE MATERIALIZED VIEW reservoir_consumer_mv TO innovacity.reservoirs
AS SELECT * FROM innovacity.reservoirs_queue;

CREATE TABLE innovacity.reservoirs1m
(
    nome_sensore String,
    timestamp1m DATETIME64,
    avgReservoir AggregateFunction(avgState, Float32),
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, nome_sensore, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.reservoirs1m_mv
TO innovacity.reservoirs1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    nome_sensore,
    avgState(value) as avgReservoir,
    latitude,
    longitude
FROM innovacity.reservoirs
GROUP BY (timestamp1m, nome_sensore, latitude, longitude);

CREATE TABLE innovacity.reservoirs_ma (
    nome_sensore String,
    timestamp1m DATETIME64,
    avgReservoir Float32,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (timestamp1m, nome_sensore, latitude, longitude);

CREATE MATERIALIZED VIEW innovacity.reservoirs1m_mov_avg
TO innovacity.reservoirs_ma
AS
SELECT
    nome_sensore,
    toStartOfMinute(timestamp) AS timestamp1m,
    avg(value) OVER (PARTITION BY  toStartOfMinute(timestamp) ORDER BY timestamp1m ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avgReservoir,
    latitude,
    longitude
FROM innovacity.reservoirs;