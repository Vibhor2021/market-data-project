CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    instrument_id VARCHAR(50),
    price FLOAT,
    volume FLOAT,
    timestamp TIMESTAMP,
    vwap FLOAT,
    is_outlier BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(instrument_id, timestamp)
);