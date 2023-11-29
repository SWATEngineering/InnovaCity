CREATE TABLE innovacity.temperatures_queue (
    timestamp DATETIME64,
    value Float32,
    type String,
    id String
) ENGINE = Kafka('kafka:9092', 'temperature', 'ch_group_1', 'JSONEachRow');

CREATE TABLE innovacity.temperatures (
    timestamp DATETIME64,
    value Float32,
    type String,
    id String
) ENGINE = MergeTree()
ORDER BY (id, timestamp);

CREATE MATERIALIZED VIEW consumer TO innovacity.temperatures
AS SELECT * FROM innovacity.temperatures_queue