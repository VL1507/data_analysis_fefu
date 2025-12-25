CREATE TABLE IF NOT EXISTS fitness_data (
    id BIGSERIAL PRIMARY KEY,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    activity VARCHAR(20) NOT NULL,
    steps INTEGER NOT NULL DEFAULT 0,
    heart_rate INTEGER,
    calories NUMERIC(6, 2) NOT NULL DEFAULT 0,
    distance_m NUMERIC(8, 2),
    speed_kmh NUMERIC(5, 2),
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION
);
CREATE INDEX IF NOT EXISTS idx_fitness_recorded_at ON fitness_data(recorded_at DESC);