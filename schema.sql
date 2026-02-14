-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========================================
-- TABLE: uploads
-- Tracks each log file ingestion event
-- =========================================
CREATE TABLE IF NOT EXISTS uploads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    total_lines INT DEFAULT 0,
    processed_bots INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- TABLE: bots
-- Stores classified bot behavior per upload
-- =========================================
CREATE TABLE IF NOT EXISTS bots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_id UUID REFERENCES uploads(id) ON DELETE CASCADE,

    ip_address TEXT NOT NULL,
    user_agent TEXT NOT NULL,

    total_requests INT NOT NULL,
    unique_urls INT NOT NULL,

    avg_url_depth FLOAT NOT NULL,
    burst_rate FLOAT NOT NULL,
    html_ratio FLOAT NOT NULL,
    repeat_url_ratio FLOAT NOT NULL,
    sitemap_hits INT DEFAULT 0,

    ai_score FLOAT NOT NULL,
    bot_type TEXT NOT NULL,               -- Indexer | Suspicious | AI_Retrieval
    confidence_level TEXT NOT NULL,       -- Low | Medium | High

    first_seen TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- INDEXES (Performance Optimization)
-- =========================================

CREATE INDEX IF NOT EXISTS idx_bots_upload_id ON bots(upload_id);
CREATE INDEX IF NOT EXISTS idx_bots_ai_score ON bots(ai_score);
CREATE INDEX IF NOT EXISTS idx_bots_bot_type ON bots(bot_type);
CREATE INDEX IF NOT EXISTS idx_bots_ip ON bots(ip_address);

-- =========================================
-- OPTIONAL FUTURE TABLE (Phase 2)
-- For storing session-level granular data
-- =========================================

CREATE TABLE IF NOT EXISTS bot_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bot_id UUID REFERENCES bots(id) ON DELETE CASCADE,
    request_count INT,
    first_seen TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sessions_bot_id ON bot_sessions(bot_id);
