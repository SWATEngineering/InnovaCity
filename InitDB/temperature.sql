CREATE TABLE innovacity.temperatures_queue (
    timestamp Float64,
    value Float32,
    type String,
    uuid UUID
) ENGINE = Kafka('kafka:9092', 'temperature', 'ch_group_1', 'JSONEachRow');

CREATE TABLE innovacity.temperatures (
    timestamp Float64,
    value Float32,
    type String,
    uuid UUID
) ENGINE = MergeTree()
ORDER BY (uuid, timestamp);

CREATE MATERIALIZED VIEW consumer TO innovacity.temperatures
AS SELECT * FROM innovacity.temperatures_queue