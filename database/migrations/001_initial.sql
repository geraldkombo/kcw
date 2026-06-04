-- Migration 001: Initial schema
-- Applied automatically by SQLiteRepository on first connect

CREATE TABLE IF NOT EXISTS farmers (
    farmer_id TEXT PRIMARY KEY,
    data TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id TEXT PRIMARY KEY,
    farmer_id TEXT NOT NULL,
    data TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pools (
    pool_id TEXT PRIMARY KEY,
    data TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id TEXT,
    data TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_loans_farmer ON loans(farmer_id);
CREATE INDEX IF NOT EXISTS idx_audit_farmer ON audit_entries(farmer_id);
