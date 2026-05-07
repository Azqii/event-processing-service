CREATE TABLE IF NOT EXISTS events (
    id UUID,
    source_id String,
    event_type String,
    event_category String,
    occurred_at DateTime,
    received_at DateTime,
    processed_at DateTime,
    processing_status String,
    payload String,
    meta String,
    error_message Nullable(String)
) ENGINE = MergeTree()
ORDER BY (occurred_at, event_type);
